def test_main():
    inputs = [
        """2
1 1 3 2
2 1 4 2
""",
        """2
1 1 3 4
3 4 6 5
""",
        """20
61 98 76 100
70 99 95 100
10 64 96 91
12 37 99 66
63 93 65 95
16 18 18 67
30 47 88 56
33 6 38 8
37 19 40 68
4 56 12 84
3 16 92 78
39 24 67 96
46 1 69 57
40 34 65 65
20 38 51 92
5 32 100 73
7 33 92 55
4 46 97 85
43 18 57 87
15 29 54 74
""",
    ]
    answers = [
        """2
1
""",
        """9
0
""",
        """1806
990
1013
1221
567
839
413
305
228
121
58
40
0
0
0
0
0
0
0
0
""",
    ]

    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        paper = []
        for i in range(N):
            paper.append(
                list(map(lambda x: int(x) - 1, text.splitlines()[i + 1].split()))
            )
        assert main(N, paper) == list(map(int, answer.splitlines()))
        assert imos_2d(N, paper) == list(map(int, answer.splitlines()))


from collections import Counter


def main(N, paper):
    # lx, ly, rx, ry
    G = [[0] * 1001 for _ in range(1001)]
    for lx, ly, rx, ry in paper:
        for x in range(lx, rx):
            for y in range(ly, ry):
                G[x][y] += 1

    c = Counter()
    for row in G:
        c += Counter(row)
    ans = []
    for i in range(1, N + 1):
        ans.append(c[i])
    return ans


from itertools import accumulate


def imos_2d(N, paper):
    G = [[0] * 1001 for _ in range(1001)]
    for lx, ly, rx, ry in paper:
        G[lx][ly] += 1
        G[rx][ry] += 1
        G[lx][ry] -= 1
        G[rx][ly] -= 1

    # cumsum of row
    for i in range(1001):
        G[i] = list(accumulate(G[i]))
    # cumsum of column
    for j in range(1001):
        cumsum = list(accumulate([G[i][j] for i in range(1001)]))
        for i in range(1001):
            G[i][j] = cumsum[i]

    c = Counter()
    for row in G:
        c += Counter(row)
    ans = []
    for i in range(1, N + 1):
        ans.append(c[i])
    return ans
