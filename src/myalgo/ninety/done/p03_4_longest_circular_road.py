from collections import deque


def test_main():
    inputs = [
        """3
1 2
2 3
    """,
        """5
1 2
2 3
3 4
3 5
""",
        """10
1 2
1 3
2 4
4 5
4 6
3 7
7 8
8 9
8 10
""",
        """31
1 2
1 3
2 4
2 5
3 6
3 7
4 8
4 9
5 10
5 11
6 12
6 13
7 14
7 15
8 16
8 17
9 18
9 19
10 20
10 21
11 22
11 23
12 24
12 25
13 26
13 27
14 28
14 29
15 30
15 31
""",
    ]

    answers = [
        3,
        4,
        8,
        9,
    ]
    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        G = [[] for _ in range(N)]
        for i in range(N - 1):
            a, b = map(int, text.splitlines()[i + 1].split())
            # as 0 index
            a -= 1
            b -= 1
            # append
            G[a].append(b)
            G[b].append(a)

        assert main(N, G) == answer


def wfs(N, G, start):
    """start"""
    maxlen = 0
    last = start
    Q = deque([(start, 0)])
    visited = [False] * N
    while Q:
        c, length = Q.popleft()
        if visited[c]:
            continue
        visited[c] = True
        length += 1
        if length > maxlen:
            maxlen = length
            last = c

        for n in G[c]:
            Q.append((n, length))

    return last, maxlen


def main(N, G):
    start, _ = wfs(N, G, 0)

    _, answer = wfs(N, G, start)

    return answer
