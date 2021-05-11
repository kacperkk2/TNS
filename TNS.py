from RBTree import RBTree
from Rule import Rule, subsume
from ArrayAlgos import contains_lex, contains_lex_plus
from copy import deepcopy
import time
import resource
import psutil


class Data:
    def __init__(self, data):
        # tidlists, each tidlist has sequences, each sequence has items
        self.tidlists = data
        self.min_item, self.max_item = self.find_min_max_items()

    def find_min_max_items(self):
        all_items = [item
                     for tidlist in self.tidlists
                     for sequence in tidlist
                     for item in sequence]
        return min(all_items), max(all_items)


class TNS:
    def __init__(self):
        self.data = None
        self.min_confidence = None
        self.delta = None
        self.k = None
        self.dynamic_min_support = 1
        self.top_k_rules = RBTree()
        self.rules_candidates = RBTree()
        self.first_occurrences = {}
        self.last_occurrences = {}

        self.start_mem = 0
        self.max_memory = 0

    def run(self, data, k, min_conf, delta):
        self.data = data
        self.delta = delta
        self.min_confidence = min_conf
        self.k = k + delta
        self.dynamic_min_support = 1
        self.first_occurrences = {}
        self.last_occurrences = {}
        self.top_k_rules = RBTree()
        self.rules_candidates = RBTree()

        self.start_mem = psutil.virtual_memory().used

        time_start = time.time()
        self.prepare_occurrences_dicts()
        self.generate_rules()
        self.crop_to_k_rules(k)
        time_end = time.time()

        return self.top_k_rules, time_end - time_start, self.max_memory

    def crop_to_k_rules(self, k):
        while self.top_k_rules.size > k:
            self.top_k_rules.pop_minimum()
        self.dynamic_min_support = self.top_k_rules.get_minimum().support

    def prepare_occurrences_dicts(self):
        for tidlist_num, tidlist in enumerate(self.data.tidlists):
            for sequence_num, sequence in enumerate(tidlist):
                for item in sequence:
                    if item not in self.first_occurrences:
                        self.first_occurrences[item] = {}
                        self.last_occurrences[item] = {}
                    if tidlist_num not in self.first_occurrences[item]:
                        self.first_occurrences[item][tidlist_num] = sequence_num
                        self.last_occurrences[item][tidlist_num] = sequence_num
                    else:
                        self.last_occurrences[item][tidlist_num] = sequence_num

    def generate_rules(self):
        for itemA in range(self.data.min_item, self.data.max_item, 1):
            if itemA not in self.first_occurrences:
                continue
            if len(self.first_occurrences[itemA]) < self.dynamic_min_support:
                continue

            for itemB in range(itemA+1, self.data.max_item+1, 1):
                if itemB not in self.first_occurrences:
                    continue
                if len(self.first_occurrences[itemB]) < self.dynamic_min_support:
                    continue

                tidlistsAB, tidlistsBA = self.find_common_tidlists(itemA, itemB)
                if tidlistsAB is None and tidlistsBA is None:
                    continue
                self.find_rule_candidates(itemA, itemB, tidlistsAB, tidlistsBA)

        while self.rules_candidates.size > 0:
            rule = self.rules_candidates.pop_maximum()
            if rule.support < self.dynamic_min_support:
                break

            if rule.expandLR:
                self.expandL(rule)
                self.expandR(rule)
            else:
                self.expandL(rule)

    def find_common_tidlists(self, itemA, itemB):
        tidlistsAB = set()
        tidlistsBA = set()
        lastAOccurrences = self.last_occurrences[itemA]
        firstAOccurrences = self.first_occurrences[itemA]
        lastBOccurrences = self.last_occurrences[itemB]
        firstBOccurrences = self.first_occurrences[itemB]

        if len(self.first_occurrences[itemA]) > len(self.first_occurrences[itemB]):
            left = len(self.first_occurrences[itemB])
            for tidlist in firstBOccurrences:
                if tidlist in firstAOccurrences:
                    firstAOccInTid = firstAOccurrences[tidlist]
                    lastAOccInTid = lastAOccurrences[tidlist]
                    firstBOccInTid = firstBOccurrences[tidlist]
                    lastBOccInTid = lastBOccurrences[tidlist]
                    if firstAOccInTid < lastBOccInTid:
                        tidlistsAB.add(tidlist)
                    if firstBOccInTid < lastAOccInTid:
                        tidlistsBA.add(tidlist)
                left -= 1
                if left + len(tidlistsAB) < self.dynamic_min_support \
                        and left + len(tidlistsBA) < self.dynamic_min_support:
                    return None, None  # try finding common tidlists for other items
        else:
            left = len(self.first_occurrences[itemA])
            for tidlist in firstAOccurrences:
                if tidlist in firstBOccurrences:
                    firstAOccInTid = firstAOccurrences[tidlist]
                    lastAOccInTid = lastAOccurrences[tidlist]
                    firstBOccInTid = firstBOccurrences[tidlist]
                    lastBOccInTid = lastBOccurrences[tidlist]
                    if firstAOccInTid < lastBOccInTid:
                        tidlistsAB.add(tidlist)
                    if firstBOccInTid < lastAOccInTid:
                        tidlistsBA.add(tidlist)
                left -= 1
                if left + len(tidlistsAB) < self.dynamic_min_support \
                        and left + len(tidlistsBA) < self.dynamic_min_support:
                    return None, None  # try finding common tidlists for other items
        return tidlistsAB, tidlistsBA

    def find_rule_candidates(self, itemA, itemB, tidlistsAB, tidlistsBA):
        AB_support = len(tidlistsAB)
        if AB_support >= self.dynamic_min_support:
            AB_confidence = float(len(tidlistsAB)) / len(self.first_occurrences[itemA])
            new_rule = Rule([itemA], [itemB], AB_confidence, AB_support,
                            self.first_occurrences[itemA].keys(), self.first_occurrences[itemB].keys(),
                            tidlistsAB, self.first_occurrences[itemA], self.last_occurrences[itemB])
            if AB_confidence >= self.min_confidence:
                self.save_to_top_k_rules(new_rule, AB_support)
            self.save_to_candidates(new_rule, expandLR=True)

        BA_support = len(tidlistsBA)
        if BA_support >= self.dynamic_min_support:
            BA_confidence = float(len(tidlistsBA)) / len(self.first_occurrences[itemB])
            new_rule = Rule([itemB], [itemA], BA_confidence, BA_support,
                            self.first_occurrences[itemB].keys(), self.first_occurrences[itemA].keys(),
                            tidlistsBA, self.first_occurrences[itemB], self.last_occurrences[itemA])
            if BA_confidence >= self.min_confidence:
                self.save_to_top_k_rules(new_rule, BA_support)
            self.save_to_candidates(new_rule, expandLR=True)

    def save_to_top_k_rules(self, rule, support):
        lower_node = self.top_k_rules.lower_node(
            Rule(None, None, 0, support+1, None, None, None, None, None)
        )
        rules_to_delete = set()
        while lower_node is not None \
                and lower_node.rule is not None \
                and lower_node.rule.support == support:
            if rule.confidence == lower_node.rule.confidence and subsume(lower_node.rule, rule):
                return
            if rule.confidence == lower_node.rule.confidence and subsume(rule, lower_node.rule):
                rules_to_delete.add(lower_node.rule)
            lower_node = self.top_k_rules.lower_node(lower_node.rule)

        for rule_to_del in rules_to_delete:
            self.top_k_rules.remove(rule_to_del)

        self.top_k_rules.add(rule)
        if self.top_k_rules.size > self.k:
            if support > self.dynamic_min_support:
                lower = self.top_k_rules.lower(
                    Rule(None, None, 0, self.dynamic_min_support+1, None, None, None, None, None)
                )
                if lower is not None:
                    self.top_k_rules.remove(lower)
                    while self.top_k_rules.size > self.k:
                        lower = self.top_k_rules.lower(
                            Rule(None, None, 0, self.dynamic_min_support + 1, None, None, None, None, None)
                        )
                        if lower is None:
                            break
                        self.top_k_rules.remove(lower)
            self.dynamic_min_support = self.top_k_rules.get_minimum().support

    def save_to_candidates(self, rule, expandLR):
        rule.expandLR = expandLR
        self.rules_candidates.add(rule)
        # memory check
        delta_mem = psutil.virtual_memory().used - self.start_mem
        if delta_mem > self.max_memory:
            self.max_memory = delta_mem

    def expandL(self, rule:Rule):
        ## Not checking max antescendants size
        frequent_items_c = {}
        left = len(rule.tidsAB)

        # work through lists where this rule applies
        for tid in rule.tidsAB:
            sequence = self.data.tidlists[tid]
            end = rule.occurrencesBlast[tid] # ending position

            # dive into the sequence
            for itemset_ind in range(end):
                itemset = sequence[itemset_ind]
                for itemC in itemset:
                    if contains_lex_plus(rule.antecedents, itemC) or contains_lex(rule.consequents, itemC):
                        continue
                
                    tids_item_c = frequent_items_c.get(itemC)
                    if tids_item_c is None:
                        if left < self.dynamic_min_support:
                            break
                    elif len(tids_item_c) + left < self.dynamic_min_support:
                        tids_item_c.remove(itemC)
                        break
                    
                    if tids_item_c is None:
                        tids_item_c = set()
                        frequent_items_c[itemC] = tids_item_c
                    tids_item_c.add(tid)
            left -= 1

        for itemC, tidsAC_B in frequent_items_c.items():
            if len(tidsAC_B) >= self.dynamic_min_support:
                tidsAC = set()
                for tid in rule.tidsA:
                    if tid in self.first_occurrences[itemC]:
                        tidsAC.add(tid)
                
                # Create rule and calculate its confidence
                confAC_B = len(tidsAC_B) / len(tidsAC)
                itemsetAC = deepcopy(rule.antecedents)
                itemsetAC.append(itemC)

                # If confidence high enough, it is a valid rule
                candidate = Rule(itemsetAC, rule.consequents, confAC_B, len(tidsAC_B), 
                                 tidsAC, None, tidsAC_B, None, rule.occurrencesBlast)
                if confAC_B >= self.min_confidence:
                    self.save_to_top_k_rules(candidate, len(tidsAC_B))
                self.save_to_candidates(candidate, expandLR=False)
        # memory check
        delta_mem = psutil.virtual_memory().used - self.start_mem
        if delta_mem > self.max_memory:
            self.max_memory = delta_mem

    def expandR(self, rule:Rule):
        ## Not checking max antescendants size
        frequent_items_c = {}
        left = len(rule.tidsAB)

        # work through lists where this rule applies
        for tid in rule.tidsAB:
            sequence = self.data.tidlists[tid]
            first = rule.occurencesAfirst[tid] # starting position

            for itemset_ind in range(first+1, len(sequence)):
                itemset = sequence[itemset_ind]
                for itemC in itemset:
                    if contains_lex(rule.antecedents, itemC) or contains_lex_plus(rule.consequents, itemC):
                        continue

                    tids_item_c = frequent_items_c.get(itemC)
                    if tids_item_c is None:
                        if left < self.dynamic_min_support:
                            continue
                    elif len(tids_item_c) + left < self.dynamic_min_support:
                        tids_item_c.remove(itemC)
                        continue
                    
                    if tids_item_c is None:
                        tids_item_c = set()
                        frequent_items_c[itemC] = tids_item_c
                    tids_item_c.add(tid)
            left -= 1

        for itemC, tidsA_BC in frequent_items_c.items():
            if len(tidsA_BC) >= self.dynamic_min_support:
                tidsBC = set()
                occurencesBC = {}

                for tid in rule.tidsB:
                    occurence_C_last = self.last_occurrences[itemC].get(tid)
                    if occurence_C_last is not None:
                        tidsBC.add(tid)
                        occurence_B_last = rule.occurrencesBlast.get(tid)
                        if occurence_C_last < occurence_B_last:
                            occurencesBC[tid] = occurence_C_last
                        else:
                            occurencesBC[tid] = occurence_B_last
                
                
                # Create rule I ==> J U{c} and calculate its confidence
                confA_BC = len(tidsA_BC) / len(rule.tidsA)
                itemsetBC = deepcopy(rule.consequents)
                itemsetBC.append(itemC)

                # if the confidence is enough
                candidate = Rule(rule.antecedents, itemsetBC, confA_BC, len(tidsA_BC),
                                rule.tidsA, tidsBC, tidsA_BC, rule.occurencesAfirst, occurencesBC)
                if confA_BC >= self.min_confidence:
                    self.save_to_top_k_rules(candidate, len(tidsA_BC))
                self.save_to_candidates(candidate, expandLR=True)
        # memory check
        delta_mem = psutil.virtual_memory().used - self.start_mem
        if delta_mem > self.max_memory:
            self.max_memory = delta_mem




