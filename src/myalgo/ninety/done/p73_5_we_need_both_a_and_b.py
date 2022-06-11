def test_main():
    inputs = [
        """7
b a b a b b a
2 1
3 7
3 2
3 4
5 4
4 6
""",
        """2
a b
1 2
""",
        """22
b a b b a b b b a b a a a a b b a b b a a a
1 7
4 14
12 22
2 4
21 17
3 20
7 8
20 14
15 11
8 14
9 12
17 8
6 20
11 20
18 19
10 8
22 20
13 21
5 14
19 20
16 14
""",
    ]
    answers = [4, 1, 16]
    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        c = text.splitlines()[1].split()
        G = [[] for _ in range(N)]
        for i in range(N - 1):
            a, b = map(lambda x: int(x) - 1, text.splitlines()[i + 2].split())
            G[a].append(b)
            G[b].append(a)
        # assert main(N, c, G) == answer
        assert tree_dp(N, c, G) == answer


from collections import deque


def get_order(N, G):
    seen = [False] * N
    order = deque([])

    def dfs(x):
        seen[x] = True
        order.append(x)
        for child in G[x]:
            if seen[child]:
                continue
            dfs(child)

    dfs(0)
    return order


def test_order():
    G = [[1, 2], [3, 4], [0], [1], [1]]
    assert get_order(5, G) == [0, 1, 3, 4, 2]


def tree_dp(N, C, G):
    dp = [[0] * 3 for _ in range(N)]
    seen = [False] * N

    def dfs(pos):
        seen[pos] = True

        # 末端の場合
        if len(G[pos]) == 1 and all([seen[c] for c in G[pos]]):
            if C[pos] == "a":
                dp[pos][0] = 1
            else:
                dp[pos][1] = 1
            return

        # 子供がいる場合
        a_or_b = 1
        both = 1
        for child in G[pos]:
            if seen[child]:
                continue
            dfs(child)

            # これで末端側からになっている
            if C[pos] == "a":
                a_or_b *= dp[child][0] + dp[child][2]
            else:
                a_or_b *= dp[child][1] + dp[child][2]
            both *= dp[child][0] + dp[child][1] + 2 * dp[child][2]

        if C[pos] == "a":
            dp[pos][0] = a_or_b
        else:
            dp[pos][1] = a_or_b
        dp[pos][2] = both - a_or_b

    dfs(0)

    # 1回dfsして順序を正しく保つ
    return dp[0][2] % (10**9 + 7)


def main(N, C, G):
    # 基本は[a,b]のグループごとに切っていく
    # 最終的なn個のグループに対してn-1本の辺があるため、2**(n-1)個に分けれる
    # ので、[a,b]に切っていく方法が肝
    # naiveには、木の端から作っていく
    #  - child = parent なら child を切っていい
    #  - child != parent になった瞬間に、そこは group として登録して次に行きたい
    #  - 孤独な child はどっかの group に併合する
    # なんとなく UnionFindぽい雰囲気を感じる
    #
    # 最初に１個 dequeに入れる
    # connection が１の場合は、それを判定 (is_groupかremoveか）
    # connectionが２の場合は、deque の最後に入れる(append_left)
    # 子供たちは左に入れる
    is_group = [False] * N
    Q = deque([0])

    while Q:
        p = Q.popleft()
        pab = C[p]
        if len(G[p]) == 0:
            continue
        if len(G[p]) == 1:
            c = G[p][0]
            cab = C[c]
            # pop
            G[p].pop()
            G[c].remove(p)

            # make group
            if cab != pab and not is_group[p]:
                is_group[c] = True

            # add to next, if is group already no hurry
            if is_group[c]:
                Q.append(c)
            else:
                Q.appendleft(c)
        else:
            # add children
            for c in G[p]:
                if len(G[c]) == 1:
                    Q.appendleft(c)
                else:
                    Q.append(c)

    return 2 ** (sum(is_group) - 1)
