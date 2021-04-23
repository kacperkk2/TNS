from RBTree import RBTree
from Rule import Rule


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

        self.prepare_occurrences_dicts()
        self.generate_rules()
        return self.top_k_rules

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

            for itemB in range(itemA+1, self.data.max_item, 1):
                if itemB not in self.first_occurrences:
                    continue
                if len(self.first_occurrences[itemB]) < self.dynamic_min_support:
                    continue

                tidlistsAB, tidlistsBA = self.find_common_tidlists(itemA, itemB)
                if tidlistsAB is None and tidlistsBA is None:
                    continue
                self.find_rule_candidates(itemA, itemB, tidlistsAB, tidlistsBA)

        while len(self.rules_candidates) > 0:
            rule = self.rules_candidates.pop_maximum()
            if rule.support < self.dynamic_min_support:
                break

            if rule.expandLR:
                expandL(rule)
                expandR(rule)
            else:
                expandL(rule)

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
            save_to_candidates(new_rule, expandLR=True)

        BA_support = len(tidlistsBA)
        if BA_support >= self.dynamic_min_support:
            BA_confidence = float(len(tidlistsBA)) / len(self.first_occurrences[itemB])
            new_rule = Rule([itemB], [itemA], BA_confidence, BA_support,
                            self.first_occurrences[itemB].keys(), self.first_occurrences[itemA].keys(),
                            tidlistsBA, self.first_occurrences[itemB], self.last_occurrences[itemA])
            if BA_confidence >= self.min_confidence:
                self.save_to_top_k_rules(new_rule, BA_support)
            save_to_candidates(new_rule, expandLR=True)

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
        if self.top_k_rules.size() > self.k:
            if support > self.dynamic_min_support:
                lower = self.top_k_rules.lower(
                    None, None, 0, self.dynamic_min_support+1, None, None, None, None, None
                )
                if lower is not None:
                    self.top_k_rules.remove(lower)
                    while self.top_k_rules.size() > self.k:
                        lower = self.top_k_rules.lower(
                            None, None, 0, self.dynamic_min_support + 1, None, None, None, None, None
                        )
                        if lower is None:
                            break
                        self.top_k_rules.remove(lower)
            self.dynamic_min_support = self.top_k_rules.get_minimum().support

    def save_to_candidates(self, rule, expandLR):
        rule.expandLR = expandLR
        self.rules_candidates.add(rule)

    def expandL(self, rule):
        # TODO
        pass

    def expandR(self, rule):
        # TODO
        pass





