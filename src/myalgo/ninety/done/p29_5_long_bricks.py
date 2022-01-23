def test_main():
    inputs = [
        """100 4
27 100
8 39
83 97
24 75
""",
        """3 5
1 2
2 2
2 3
3 3
1 2
""",
        """10 10
1 3
3 5
5 7
7 9
2 4
4 6
6 8
3 5
5 7
4 6
""",
        """500000 7
1 500000
500000 500000
1 500000
1 1
1 500000
500000 500000
1 500000
""",
    ]
    answers = [
        """1
2
2
3
""",
        """1
2
3
4
4
""",
        """1
2
3
4
3
4
5
5
6
7
""",
        """1
2
3
4
5
6
7
""",
    ]

    for text, answer in zip(inputs, answers):
        W, N = map(int, text.splitlines()[0].split())
        bricks = []
        for i in range(N):
            L, R = map(int, text.splitlines()[i + 1].split())
            bricks.append((L, R))

        expected = list(map(int, answer.splitlines()))
        actual = main(bricks)
        assert actual == expected


def main(big_bricks):
    # 範囲の最大値と範囲への加算
    # 何かしらの木構造 -> segmentTree (range update query)
    bricks, W = compress(big_bricks)
    ans = []
    tree = RUQ(W)
    for left, right in bricks:
        current = tree.query(left, right + 1)
        tree.update(left, right + 1, current - 1)
        ans.append(-current + 1)
    return ans


def compress(bricks):
    """座標圧縮をする必要がある
    compress したものを返してあげれば、RUQは何も気にせずやれる
    decompressは必要ない
    """
    all_values = set()
    for left, right in bricks:
        all_values.add(left)
        all_values.add(right)

    # sort and index
    index = {k: i for i, k in enumerate(sorted(all_values))}
    res = []
    for left, right in bricks:
        res.append((index[left], index[right]))
    return res, len(all_values)


def test_compress():
    assert compress([(0, 1), (2, 4), (8, 16)]) == ([(0, 1), (2, 3), (4, 5)], 6)
    assert compress([(0, 1), (2, 2), (8, 10)]) == ([(0, 1), (2, 2), (3, 4)], 5)


class RUQ:
    def __init__(self, W):
        self.INF = 0
        self.W = W
        n, i = get_m(W)
        self.n = n
        self.nodes = [self.INF] * (2 * n - 1)
        self.lazy = [self.INF] * (2 * n - 1)

    def query(self, a, b):
        return self.query_sub(a, b, 0, 0, self.n)

    def update(self, a, b, x):
        self.update_sub(a, b, x, 0, 0, self.n)

    def eval(self, k):
        if self.lazy[k] == self.INF:
            return
        if k < self.n - 1:
            self.lazy[k * 2 + 1] = self.lazy[k]
            self.lazy[k * 2 + 2] = self.lazy[k]
        self.nodes[k] = self.lazy[k]
        self.lazy[k] = self.INF

    def query_sub(self, a, b, k, l, r):
        self.eval(k)
        if r <= a or b <= l:
            return self.INF
        if a <= l and r <= b:
            return self.nodes[k]
        vl = self.query_sub(a, b, k * 2 + 1, l, (l + r) // 2)
        vr = self.query_sub(a, b, k * 2 + 2, (l + r) // 2, r)
        return min(vl, vr)

    def update_sub(self, a, b, x, k, l, r):
        self.eval(k)
        if a <= l and r <= b:  # 完全に内側の時
            self.lazy[k] = x
            self.eval(k)
            return
        if a < r and l < b:
            self.update_sub(a, b, x, k * 2 + 1, l, (l + r) // 2)
            self.update_sub(a, b, x, k * 2 + 2, (l + r) // 2, r)
            self.nodes[k] = min(self.nodes[k * 2 + 1], self.nodes[k * 2 + 2])
            return


class RSQ:
    def __init__(self, W):
        self.W = W
        M, n = get_m(W)
        self.n = n
        self.nodes = [None] * (2 * n - 1)

    def update(self, i, x):
        i += self.n - 1
        self.nodes[i] = x
        while i > 0:
            i = (i - 1) // 2  # parent
            self.nodes[i] = min(self.nodes[i * 2 + 1], self.nodes[i * 2 + 2])

    def query(self, a, b):
        return self.query_sub(a, b, 0, 0, self.n)

    def query_sub(self, a, b, k, l, r):
        if r <= a or b <= l:
            return 1 << 32
        if a <= l and r <= b:
            return self.nodes[k]
        vl = self.query_sub(a, b, k * 2 + 1, l, (l + r) // 2)
        vr = self.query_sub(a, b, k * 2 + 2, (l + r) // 2, r)
        return min(vl, vr)


def get_m(N):
    i = 0
    while (1 << i) < N:
        i += 1
    M = 1 << i
    return M, i


def test_get_m():
    assert get_m(4) == (4, 2)
    assert get_m(3) == (4, 2)
    assert get_m(10) == (16, 4)


def test_nums():
    print()
    print(1 << 2)
    print(1 >> 2)
