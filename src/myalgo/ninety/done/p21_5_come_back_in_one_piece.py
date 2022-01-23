def test_main():
    inputs = [
        """4 7
1 2
2 1
2 3
4 3
4 1
1 4
2 3
""",
        """100 1
1 2
""",
    ]
    answers = [3, 0]
    for text, answer in zip(inputs, answers):
        N, M = map(int, text.splitlines()[0].split())
        G = [[] for _ in range(N)]
        H = [[] for _ in range(N)]
        for i in range(M):
            a, b = map(lambda x: int(x) - 1, text.splitlines()[i + 1].split())
            G[a].append(b)
            H[b].append(a)

        # assert main(N, G) == answer
        s = SCC(N, G, H)
        s.main()
        assert s.answer == answer


from collections import deque


class Loop:
    def __init__(self, N, G):
        self.N = N
        self.G = G
        self.used = [False] * N
        self.in_loop = [False] * N

    def dfs(self, start, current, path):
        if start == current and self.used[current]:
            return path
            # for p in path self.in_loop[p] = True
        self.used[current] = True
        for child in self.G[current]:
            if start != child and self.used[child]:
                continue
            path = self.dfs(start, child, path)
            path.append(child)
        self.used[current] = False
        return path


class SCC:
    def __init__(self, N, G, H):
        self.N = N
        self.G = G
        self.H = H
        self.used = [False] * N
        self.order = []
        self.count = 0
        self.answer = 0

    def dfs(self, v):
        self.used[v] = True
        for child in self.G[v]:
            if not self.used[child]:
                self.dfs(child)
        self.order.append(v)

    def dfs2(self, v):
        self.used[v] = True
        self.count += 1
        for child in self.H[v]:
            if not self.used[child]:
                self.dfs2(child)

    def main(self):
        # first dfs
        for i in range(self.N):
            if not self.used[i]:
                self.dfs(i)
        # second dfs
        self.order = self.order[::-1]
        self.used = [False] * self.N
        for i in self.order:
            if self.used[i]:
                continue
            self.count = 0
            self.dfs2(i)
            self.answer += self.count * (self.count - 1) // 2
        return self.answer


def main(N, G):
    # must be a loop
    # for all loops starting from N, add the length of them
    in_loop = [False] * N
    loops = []

    for i in range(N):
        if in_loop[i]:
            continue
        visited = [False] * N
        Q = deque([i])
        while Q:
            if visited[i]:
                continue
            visited[i] = True
        # loop = [i for i, e in enumuerate(visited) if e]
