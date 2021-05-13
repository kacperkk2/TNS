from get_data import get_data
from TNS import TNS, Data

if __name__ == '__main__':
    # IMPORTANT: tidlists elements should be in lexical order
    # (need to remember when load data from external resource)

    # TODO
    # IMPORTANT: if we load text we should give biggest lexicographical word the bigger number in data
    tidlists = [
        [[1], [1,2,3], [1,3], [4], [3,6]],
        [[1,4], [3], [2,3], [1,5]],
        [[5,6], [1,2], [4,6], [3], [2]],
        [[5], [7], [1,6], [3], [2], [3]],
    ]
    tidlists = get_data()
    data = Data(tidlists)
    algorithm = TNS()
    rules, exec_time_seconds, memory_usage_bytes = algorithm.run(data, k=1000, min_conf=0.8, delta=2)
    # print(rules)
    print(exec_time_seconds, "s")
    print(memory_usage_bytes, "bytes")

