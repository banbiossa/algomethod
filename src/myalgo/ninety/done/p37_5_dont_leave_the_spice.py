def test_main():
    inputs = [
        """100 4
30 40 120
30 40 30
30 40 1500
30 40 40
""",
        """100 4
13 15 31415
12 13 92653
29 33 58979
95 98 32384
""",
        """5000 5
1000 1000 1000000000
1000 1000 1000000000
1000 1000 1000000000
1000 1000 1000000000
1000 1000 1000000000
""",
        """10000 20
4539 6002 485976
1819 5162 457795
1854 2246 487643
1023 4733 393530
1052 6274 289577
1874 2436 167747
1457 4248 452660
2103 4189 174955
3057 5061 319316
4898 4953 394627
1313 2880 154687
1274 1364 259598
3866 5844 233027
1163 5036 386223
1234 4630 155972
2845 4978 442858
3168 5368 171601
3708 4407 394899
3924 4122 428313
2112 4169 441976
""",
    ]
    answers = [
        1660,
        -1,
        5000000000,
        2727026,
    ]

    for text, answer in zip(inputs, answers):
        W, N = map(int, text.splitlines()[0].split())
        query = []
        for i in range(N):
            l, r, v = map(int, text.splitlines()[i + 1].split())
            query.append((l, r, v))
        # assert main(W, N, query) == answer
        assert with_segment_tree(W, N, query) == answer


def main(W, N, query):
    # dp でやれる気がする
    dp = [[-1 << 32] * (W + 1) for _ in range(N + 1)]
    dp[0][0] = 0

    for i in range(N):
        for j in range(W):
            if dp[i][j] == -1 << 32:
                continue
            # 下に伸ばす
            dp[i + 1][j] = max(dp[i][j], dp[i + 1][j])

            # i番目のquery分だけ伸ばす
            l, r, v = query[i]
            for k in range(l, r + 1):
                if j + k > W:
                    break
                dp[i + 1][j + k] = max(dp[i][j] + v, dp[i + 1][j + k])

    if dp[-1][-1] == -1 << 32:
        return -1
    return dp[-1][-1]


class SegTree:
    """
    init(init_val, ide_ele): 配列init_valで初期化 O(N)
    update(k, x): k番目の値をxに更新 O(logN)
    query(l, r): 区間[l, r)をsegfuncしたものを返す O(logN)
    """

    def __init__(self, init_val, segfunc, ide_ele):
        """
        init_val: 配列の初期値
        segfunc: 区間にしたい操作
        ide_ele: 単位元
        n: 要素数
        num: n以上の最小の2のべき乗
        tree: セグメント木(1-index)
        """
        n = len(init_val)
        self.segfunc = segfunc
        self.ide_ele = ide_ele
        self.num = 1 << (n - 1).bit_length()
        self.tree = [ide_ele] * 2 * self.num
        # 配列の値を葉にセット
        for i in range(n):
            self.tree[self.num + i] = init_val[i]
        # 構築していく
        for i in range(self.num - 1, 0, -1):
            self.tree[i] = self.segfunc(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, k, x):
        """
        k番目の値をxに更新
        k: index(0-index)
        x: update value
        """
        k += self.num
        self.tree[k] = x
        while k > 1:
            self.tree[k >> 1] = self.segfunc(self.tree[k], self.tree[k ^ 1])
            k >>= 1

    def get(self, k):
        k += self.num
        return self.tree[k]

    def query(self, l, r):
        """
        [l, r)のsegfuncしたものを得る
        l: index(0-index)
        r: index(0-index)
        """
        l = max(0, l)
        r = min(r, self.num)
        res = self.ide_ele

        l += self.num
        r += self.num
        while l < r:
            if l & 1:
                res = self.segfunc(res, self.tree[l])
                l += 1
            if r & 1:
                res = self.segfunc(res, self.tree[r - 1])
            l >>= 1
            r >>= 1
        return res


def with_segment_tree(W, N, query):
    # lookup の部分を segment_tree 化する
    dp_array = [[-1 << 32] * (W + 1) for _ in range(N + 1)]
    dp_array[0][0] = 0

    # 各行を segment_tree として初期化
    # dp[i][j] = dp[i-1][j]
    # dp[i][j] = max(dp[i-1][j-R_i], ..., dp[i-1][j-L_i]) + V_i を高速化
    dp = []
    for row in dp_array:
        dp.append(SegTree(row, max, -1 << 32))

    # 貰うdpにする
    for i in range(1, N + 1):
        for j in range(W + 1):
            # 下に伸ばす
            best = dp[i - 1].get(j)
            current = dp[i].get(j)
            if current < best and best >= 0:
                dp[i].update(j, best)

            answer = dp[-1].get(W)

            # range max
            l, r, v = query[i - 1]
            left = max(j - r, 0)
            right = min(j - l, W + 1)  # 右に出過ぎないように
            if left > right:
                continue

            # 現状よりよくなければアップデートしない(debugしやすさのため)
            best = dp[i - 1].query(left, right + 1) + v
            current = dp[i].get(j)
            if current < best and best >= 0:
                dp[i].update(j, best)

    if dp[-1].get(W) == -1 << 32:
        return -1
    return dp[-1].get(W)
