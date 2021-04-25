
def subsume(rule1, rule2):
    if len(rule1.antecedents) <= len(rule2.antecedents) \
            and len(rule1.consequents) >= len(rule2.consequents):
        rule2_ant_contain_rule1_ant = \
            all(ant in rule2.antecedents for ant in rule1.antecedents)
        rule1_con_contain_rule2_con = \
            all(con in rule1.consequents for con in rule2.consequents)
        return rule2_ant_contain_rule1_ant and rule1_con_contain_rule2_con
    return False

count = 0

class Rule:
    def __init__(self, antecedents, consequents, confidence, support,
                 tidsA, tidsB, tidsAB, occurencesAfirst, occurrencesBlast):
        global count
        self.antecedents = antecedents
        self.consequents = consequents
        self.confidence = confidence
        self.support = support
        self.tidsA = tidsA
        self.tidsB = tidsB
        self.tidsAB = tidsAB
        self.occurencesAfirst = occurencesAfirst
        self.occurrencesBlast = occurrencesBlast
        self.expandLR = False
        self.count = count
        count += 1

    def __str__(self):
        ant = ','.join(str(x) for x in self.antecedents)
        con = ','.join(str(x) for x in self.consequents)
        return ant + " ==> " + con
    
    def compare(self, o):
        if o is self:
            return 0
        compare = self.support - o.support
        if compare != 0:
            return compare
        itemset1sizeA = 0 if self.antecedents is None else len(self.antecedents)
        itemset1sizeB = 0 if o.antecedents is None else len(o.antecedents)
        compare2 = itemset1sizeA - itemset1sizeB
        if compare2 != 0:
            return compare2

        itemset2sizeA = 0 if self.consequents is None else len(self.consequents)
        itemset2sizeB = 0 if o.consequents is None else len(o.consequents)
        compare3 = itemset2sizeA - itemset2sizeB
        if compare3 != 0:
            return compare3

        compare4 = self.confidence - o.confidence
        if compare4 != 0:
            return compare4

        return self.count - o.count
