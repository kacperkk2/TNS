from RBTree import RBTree


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
        pass
