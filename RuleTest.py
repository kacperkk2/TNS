from Rule import Rule


def empty_rules_equals():
    rule1 = Rule([], [], 0, 0, None, None, None, None, None)
    rule2 = Rule([], [], 0, 0, None, None, None, None, None)
    assert rule1.compare(rule2) == 0


def non_empty_rules_equals():
    rule1 = Rule([1,4,6], [11,2,4], 1.0, 5, [0,1], [0,1], [0,1], {1: 1111}, {2:1})
    rule2 = Rule([7,8,999], [55,6,777], 1.0, 5, [0,2], [0,3], [0,4], {1: 22222}, {2:1})
    assert rule1.compare(rule2) == 0


def rules_different_confidence():
    rule1 = Rule([1,2,3], [5,6,7], 1.0, 5, [0,1], [0,1], [0,1], {1: 0}, {2:1})
    rule2 = Rule([1,2,3], [5,6,7], 0.99, 5, [0,1], [0,1], [0,1], {1: 0}, {2:1})
    assert rule1.compare(rule2) > 0


def rules_different_antecents():
    rule1 = Rule([1,2,3,4], [5,6,7], 1.0, 5, [0,1], [0,1], [0,1], {1: 0}, {2:1})
    rule2 = Rule([1,2,3], [5,6,7], 1.0, 5, [0,1], [0,1], [0,1], {1: 0}, {2:1})
    assert rule1.compare(rule2) > 0


def rules_different_conseqents():
    rule1 = Rule([1,2,3], [5,6,7,5], 1.0, 5, [0,1], [0,1], [0,1], {1: 0}, {2:1})
    rule2 = Rule([1,2,3], [5,6,7], 1.0, 5, [0,1], [0,1], [0,1], {1: 0}, {2:1})
    assert rule1.compare(rule2) > 0


def rules_different_support():
    rule1 = Rule([1,2,3], [5,6,7], 1.0, 5, [0,1], [0,1], [0,1], {1: 0}, {2:1})
    rule2 = Rule([1,2,3], [5,6,7], 1.0, 4, [0,1], [0,1], [0,1], {1: 0}, {2:1})
    assert rule1.compare(rule2) > 0


if __name__ == '__main__':
    empty_rules_equals()
    non_empty_rules_equals()
    rules_different_confidence()
    rules_different_antecents()
    rules_different_support()