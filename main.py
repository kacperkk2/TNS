from get_data import get_data
from TNS import TNS, Data
from TNS_prev import TNS as TNS_prev
import sys

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
    print("Args:", sys.argv)
    print("Input file:", sys.argv[1])
    print("k:", sys.argv[2])
    min_conf = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8
    print("min_conf:", min_conf)
    delta = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    print("delta:", delta)
    algo_ver = sys.argv[5] if len(sys.argv) > 5 else 'ETARM'
    print("algo_ver:", algo_ver)

    tidlists = get_data(sys.argv[1])
    data = Data(tidlists)
    algorithm = TNS() if algo_ver == 'ETARM' else TNS_prev()
    rules, exec_time_seconds, memory_usage_bytes = algorithm.run(data, k=int(sys.argv[2]), min_conf=min_conf, delta=delta)
    # print(rules)
    print(str(rules)[:200])
    print(rules.size)
    print(exec_time_seconds, "s")
    print(memory_usage_bytes, "bytes")

