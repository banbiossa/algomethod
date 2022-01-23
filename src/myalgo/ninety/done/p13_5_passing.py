def test_main():
    inputs = [
        """7 9
1 2 2
1 3 3
2 5 2
3 4 1
3 5 4
4 7 5
5 6 1
5 7 6
6 7 3
""",
        """4 3
1 2 1
2 3 10
3 4 100
""",
        """4 3
1 2 314
1 3 159
1 4 265
""",
    ]
    answers = [
        """8
8
9
9
8
8
8
""",
        """111
111
111
111
""",
        """265
893
583
265
""",
    ]

    for text, answer in zip(inputs, answers):
        N, M = map(int, text.splitlines()[0].split())
        G = [[] for _ in range(N)]
        for i in range(M):
            a, b, c = map(int, text.splitlines()[i + 1].split())
            a -= 1
            b -= 1
            G[a].append((b, c))
            G[b].append((a, c))
        assert main(N, G) == list(map(int, answer.split()))


from collections import deque
from heapq import heappop, heappush


def dijkstra(N, G, i):
    dist = [1 << 32] * N
    dist[i] = 0
    h = []
    heappush(h, (0, i))
    while h:
        _, pos = heappop(h)
        for to, cost in G[pos]:
            if dist[to] > dist[pos] + cost:
                dist[to] = dist[pos] + cost
                heappush(h, (dist[to], to))
    return dist


def main(N, G):
    from_1 = dijkstra(N, G, 0)
    to_N = dijkstra(N, G, N - 1)
    ans = []
    for i in range(N):
        ans.append(from_1[i] + to_N[i])
    return ans


def _main(N, M, T, G):
    print(N, M, T, G)
    # 方針:
    #   1: 1->k k->Nの最短経路を持つ
    #   2: 再度 from_1,to_N に入っている場合は、それを利用していい
    from_1 = wfs(N, T, G, 0)
    to_N = wfs(N, T, G, N - 1)
    ans = []
    for i in range(N):
        ans.append(from_1[i] + to_N[i])
    return ans


def wfs(N, T, G, i):
    dist = [1 << 32] * N
    dist[i] = 0
    Q = deque([i])
    while Q:
        j = Q.popleft()
        for child in G[j]:
            if dist[j] + T[j][child] < dist[child]:
                dist[child] = dist[j] + T[j][child]
                Q.append(child)
    return dist
