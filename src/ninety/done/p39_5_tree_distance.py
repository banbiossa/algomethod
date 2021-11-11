def test_main():
    inputs = [
        """2
1 2
""",
        """4
1 2
1 3
1 4
""",
        """12
1 2
3 1
4 2
2 5
3 6
3 7
8 4
4 9
10 5
11 7
7 12
""",
    ]
    answers = [1, 9, 211]
    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        G = [[] for _ in range(N)]
        for i in range(N - 1):
            a, b = map(lambda x: int(x) - 1, text.splitlines()[i + 1].split())
            G[a].append(b)
            G[b].append(a)
        t = TreeDist(N, G)
        t.main()
        assert t.answer == answer


class TreeDist:
    def __init__(self, N, G):
        self.N = N
        self.G = G
        self.dp = [0] * N
        self.answer = None

    def dfs(self, pos, pre):
        # dp[x] = 1 + sum(dp[部下])
        self.dp[pos] = 1
        # 直属の部下を巡る
        for i in self.G[pos]:
            if i == pre:
                continue
            self.dfs(i, pos)
            self.dp[pos] += self.dp[i]

    def calc(self):
        # |A| * (N-|A|)のsumを取る
        ans = sum(self.dp[i] * (self.N - self.dp[i]) for i in range(self.N))
        self.answer = ans
        return ans

    def main(self):
        self.dfs(0, 0)  # pos, pre は要検討
        return self.calc()


def test_sum():
    assert sum([]) == 0
    assert sum([i for i in range(0)]) == 0
