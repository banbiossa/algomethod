def test_main():
    inputs = [
        """3 3
1 2
1 3
2 3
""",
        """2 1
1 2
""",
        """7 7
1 2
2 3
3 4
4 2
5 6
6 7
7 5
""",
    ]
    answers = [2, 0, 4]
    for text, answer in zip(inputs, answers):
        N, M = map(int, text.splitlines()[0].split())
        G = [[] for _ in range(N)]
        for i in range(M):
            u, v = map(lambda x: int(x) - 1, text.splitlines()[i + 1].split())
            G[u].append(v)
            G[v].append(u)
        # assert main(N, M, G) == answer
        main(N, M, G) == answer


def main(N, M, G):
    # 枝刈り（長さが１のものはいらない）
    print(N, M, G)

    for i, v in enumerate(G):
        if len(v) != 1:
            continue
        # 長さは1
        u = v.pop()
        G[u].remove(i)

    print(N, M, G)
    # 長さが2以外の頂点は存在しない
    for i, v in enumerate(G):
        if len(v) != 0 and len(v) != 2:
            return 0

    # これで閉路のみになった
    # 2**閉路数が答え
    visited = [False] * N
    num = 0
    for i in range(N):
        if visited[i]:
            continue
        visited[i] = True
        if len(G[i]) == 0:
            continue
