
def contains_lex_plus(itemset, searched_item):
    for item in itemset:
        if item == searched_item:
            return True
        if item > searched_item:
            return True
    return False

def contains_lex(itemset, searched_item):
    for item in itemset:
        if item == searched_item:
            return True
        if item > searched_item:
            return False
    return False