def test_main():
    inputs = [
        """3 3
-1 2
1 1
-2 -3
1
2
3
""",
        """5 3
-2 -2
-1 -1
0 0
1 1
2 2
5
3
1
""",
        """2 1
-1000000000 -1000000000
1000000000 1000000000
1
""",
    ]
    answers = [
        """6
7
7
""",
        """8
4
8
""",
        "4000000000",
    ]

    for text, answer in zip(inputs, answers):
        N, Q = map(int, text.splitlines()[0].split())
        G = []
        for i in range(N):
            x, y = map(int, text.splitlines()[i + 1].split())
            G.append((x, y))
        queries = []
        for i in range(Q):
            q = int(text.splitlines()[i + N + 1]) - 1
            queries.append(q)

        assert main(N, Q, G, queries) == list(map(int, answer.splitlines()))
        assert N_square(N, Q, G, queries) == list(map(int, answer.splitlines()))


def manhattan(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def N_square(N, Q, G, queries):
    ans = []
    for i in queries:
        furthest = 0
        for j in range(N):
            furthest = max(furthest, manhattan(G[i], G[j]))
        ans.append(furthest)
    return ans


def trumps(x, y, xn, yn):
    """元のに加えて、xnew,ynewがどんな存在か"""
    if x * xn < 0 or y * yn < 0:
        return "different"  # 象限が違う

    x, y, xn, yn = (abs(i) for i in (x, y, xn, yn))

    if x >= xn and y >= yn:
        return "bad"  # 使わない

    if x <= xn and y <= yn:
        return "trumps"  # 使う、かつ元のを削除する

    return "new"  # 新たに仲間に加える


def test_trumps():
    assert trumps(1, 1, 2, 3) == "trumps"
    assert trumps(1, 1, 2, 1) == "trumps"
    assert trumps(2, 2, 2, 1) == "bad"
    assert trumps(2, 2, -2, 1) == "different"
    assert trumps(-2, -2, -3, -3) == "trumps"


def main(N, Q, G, queries):
    # 45度回転させて、max,minと比較
    H = []
    for x, y in G:
        H.append((x - y, x + y))

    X_max = max([x for x, y in H])
    X_min = min([x for x, y in H])
    Y_max = max([y for x, y in H])
    Y_min = min([y for x, y in H])

    ans = []
    for q in queries:
        x, y = H[q]
        ans.append(max(abs(X_max - x), abs(X_min - x), abs(Y_max - y), abs(Y_min - y)))
    return ans
