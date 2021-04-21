from TNS import TNS, Data

if __name__ == '__main__':
    tidlists = [
        [[1], [1,2,3], [1,3], [4], [3,6]],
        [[1,4], [3], [2,3], [1,5]],
        [[5,6], [1,2], [4,6], [3], [2]],
        [[5], [7], [1,6], [3], [2], [3]],
    ]
    data = Data(tidlists)
    algorithm = TNS()
    algorithm.run(data, k=10, min_conf=0.5, delta=40)

