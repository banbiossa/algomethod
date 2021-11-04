def test_main():
    inputs = [
        """4
1 2
2 3
2 4
""",
        """6
1 3
2 4
3 5
2 5
3 6
""",
    ]
    answers = ["3 4", "1 2 6"]
    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        G = [[] for _ in range(N)]
        for i in range(N - 1):
            a, b = map(int, text.splitlines()[i + 1].split())
            a -= 1
            b -= 1
            G[a].append(b)
            G[b].append(a)
        # assert main(N, G) == list(map(int, answer.split()))
        # t = Tree(N, G)
        # print(t.solve())
        # print(main(N, G) == list(map(int, answer.split())))

        g = Graph(N, G)
        ans = g.solve()
        print([i + 1 for i in ans[0 : (N // 2)]])


class Graph:
    def __init__(self, N, G):
        self.N = N
        self.G = G
        self.col = [-1] * N

    def dfs(self, pos, cur):
        self.col[pos] = cur
        for i in self.G[pos]:
            if self.col[i] == -1:
                self.dfs(i, 1 - cur)

    def solve(self):
        # 0 を 0 で色付ける
        self.dfs(0, 0)
        if self.col.count(0) >= (self.N // 2):
            colour = 0
        else:
            colour = 1
        ans = [i for i, c in enumerate(self.col) if c == colour]
        return ans


def rem(G, a):
    """remove node a from graph G"""
    for child in G[a]:
        G[child].remove(a)
    G[a] = []
    return G


class Tree:
    def __init__(self, N, G):
        self.N = N
        self.G = G

    def rem(self, a):
        """remove node a from graph G"""
        for child in self.G[a]:
            self.G[child].remove(a)
        self.G[a] = []

    def solve(self):
        ans = []
        for i in range(self.N // 2):
            if len(self.G[i]) <= 1:
                ans.append(i)
                # remove parent
                for parent in self.G[i]:
                    self.rem(parent)
        return ans


def test_rem():
    t = Tree(3, [[1], [0]])
    t.rem(0)
    assert t.G[0] == []
    assert t.G[1] == []
