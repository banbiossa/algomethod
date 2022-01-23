def test_main():
    inputs = [
        """3
1 10 100
10 1 100
100 10 1
1
1 2
""",
        """4
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 16
3
1 2
1 3
2 3
""",
        """3
1 10 100
10 1 100
100 10 1
0
""",
    ]
    outputs = [111, -1, 3]
    for text, answer in zip(inputs, outputs):
        N = int(text.splitlines()[0])
        A = []
        for i in range(N):
            A.append(list(map(int, text.splitlines()[i + 1].split())))
        M = int(text.splitlines()[N + 1])
        G = set()
        for i in range(M):
            x, y = map(lambda x: int(x) - 1, text.splitlines()[i + N + 2].split())
            # force x < y
            G.add((x, y))
            G.add((y, x))

        assert main(N, A, M, G) == answer


import itertools


def main(N, A, M, G):
    print(N, A, M, G)
    # 全探索する
    best = N * 1000
    found = False
    for order in itertools.permutations(range(N)):
        if is_ok(order, G):
            current = calc_time(order, A)
            found = True
            best = min(current, best)

    if not found:
        return -1
    return best


def is_ok(order, G):
    for i in range(len(order) - 1):
        if (order[i], order[i + 1]) in G:
            return False
    return True


def calc_time(order, A):
    time = 0
    for i, p in enumerate(order):
        time += A[p][i]
    return time
