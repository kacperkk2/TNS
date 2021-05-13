def get_data():
    with open('experiments/number_data/chess.txt', mode='r') as txtfile:
        lines = txtfile.readlines()
        tidlists = [[[int(elem)] for elem in line.split(' ') if elem.isdigit()] for line in lines]
        # print(tidlists[:10])
        # exit(0)
        print("Got data")
        print(len(tidlists))
        # print(tidlists[0])
        # exit(0)
        return tidlists