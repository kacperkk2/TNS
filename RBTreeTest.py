from RBTree import RBTree
from Rule import Rule


def only_root_tree():
    tree = RBTree()
    rule = Rule([1,2,3], [5,6], 0, 0, None, None, None, None, None)
    tree.add(rule)
    assert tree.size == 1
    assert tree.root.rule is rule
    print(tree)


def two_elements_in_tree():
    tree = RBTree()
    rule1 = Rule([1,2,3], [5,6], 0, 0, None, None, None, None, None)
    rule2 = Rule([1,2,3], [5,6,7], 1.0, 0, None, None, None, None, None)
    tree.add(rule1)
    tree.add(rule2)
    assert tree.root.rule == rule1
    assert tree.root.right.rule == rule2
    assert tree.root.left is None
    print(tree)

    tree = RBTree()
    rule1 = Rule([1, 2, 3], [5, 6, 7], 1.0, 0, None, None, None, None, None)
    rule2 = Rule([1, 2, 3], [5, 6], 0, 0, None, None, None, None, None)
    tree.add(rule1)
    tree.add(rule2)
    assert tree.root.rule == rule1
    assert tree.root.right is None
    assert tree.root.left.rule == rule2
    print(tree)


def multiple_elements_in_tree():
    tree = RBTree()
    rule1 = Rule([1, 2, 3], [5, 6, 7], 1.0, 0, None, None, None, None, None)
    rule2 = Rule([1, 2, 3], [5, 6], 0, 0, None, None, None, None, None)
    rule3 = Rule([1, 2, 3, 4, 5], [5], 0, 0, None, None, None, None, None)
    rule4 = Rule([1], [5], 0, 0, None, None, None, None, None)
    tree.add(rule1)
    tree.add(rule2)
    tree.add(rule3)
    tree.add(rule4)
    assert tree.size == 4
    assert tree.root.rule == rule1
    assert tree.root.left.rule == rule2
    assert tree.root.right.rule == rule3
    assert tree.root.left.left.rule == rule4

    assert tree.get_minimum() == rule4
    assert tree.get_maximum() == rule3

    poped_rule = tree.pop_maximum()
    assert poped_rule == rule4
    assert tree.size == 3
    print(tree)


if __name__ == '__main__':
    # only_root_tree()
    # two_elements_in_tree()
    multiple_elements_in_tree()
