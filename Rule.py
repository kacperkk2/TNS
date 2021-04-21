
class Rule:
    def __init__(self, antecedents, consequents, confidence, support,
                 tidsA, tidsB, tidsAB, occurencesAfirst, occurrencesBlast):
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

        return 0
