def test_main():
    inputs = [
        """4
7
0 1 2 3
1 1 2 1
1 3 4 5
0 3 4 6
1 3 4 5
0 2 3 6
1 3 1 5
""",
        """15
25
0 11 12 41
0 1 2 159
0 14 15 121
0 4 5 245
0 12 13 157
0 9 10 176
0 6 7 170
0 2 3 123
0 7 8 167
0 3 4 159
1 12 11 33
0 10 11 116
0 8 9 161
1 9 12 68
1 12 12 33
1 7 12 74
0 5 6 290
1 8 9 93
0 13 14 127
1 10 12 108
1 14 1 3
1 13 8 124
1 12 11 33
1 12 10 33
1 5 15 194
""",
    ]
    answers = [
        """2
Ambiguous
1
2
""",
        """8
33
33
33
68
33
144
93
8
108
118
""",
    ]
    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        N += 1
        Q = int(text.splitlines()[1])
        query = []
        query0 = []
        for i in range(Q):
            query.append(list(map(int, text.splitlines()[i + 2].split())))
            if query[-1][0] == 0:
                query0.append(query[-1])
        # ans = main(N, query)
        # ans = with_segment_tree(N, query)
        ans = ac(N, query, query0)
        assert ans == answer.splitlines()


def ac(N, query, query0):
    # unionFindで1周する
    # 次に全てのクエリを先に処理し、関係性を割り出す
    # 1度関係を固定させ、+1, -1の関係性から答えを求める
    tree = UnionFind(N)
    ans = []
    A = [0] * N

    # クエリ先読み
    query0.sort()
    for _, x, y, v in query0:
        A[y] = v - A[x]

    for i, q in enumerate(query):
        t, x, y, v = q
        if t == 0:
            tree.unite(x, y)
        if t == 1:
            if not tree.issame(x, y):
                ans.append("Ambiguous")
            else:
                diff = v - A[x]
                if abs(x - y) % 2 == 0:
                    ans.append(str(A[y] + diff))
                else:
                    ans.append(str(A[y] - diff))
    return ans


class UnionFind:
    def __init__(self, n):
        self.par = [-1] * n
        self.rank = [0] * n

    def root(self, x):
        if self.par[x] == -1:
            return x  # x が根の場合は x を返す
        else:
            self.par[x] = self.root(self.par[x])  # 経路圧縮
            return self.par[x]

    def issame(self, x, y):
        return self.root(x) == self.root(y)

    def unite(self, x, y):
        rx = self.root(x)
        ry = self.root(y)
        if rx == ry:
            return False  # すでに同じグループのときは何もしない
        if self.rank[rx] > self.rank[ry]:  # ry 側の rank が小さくなるようにする
            rx, ry = ry, rx
        self.par[ry] = rx  # ry を rx の子とする
        if self.rank[rx] == self.rank[ry]:  # rx 側の rank を調整する
            self.rank[rx] += 1
        return True


def main(N, query):
    # 自前クラスでambiguityを管理
    # sums[i] = v -> a[i]+a[i+1]=vを表現
    checkers = [None] * N
    ans = []
    for q in query:
        t, x, y, v = q
        if t == 0:
            # 交互に+/-で持っている必要があるため
            checkers[x] = v if x % 2 == 0 else -v
        if t == 1:
            ans.append(str(one_query(x, y, v, checkers)))
    return ans


from math import nan, isnan


# segfunc
def take_sum(x, y):
    return x + y


def with_segment_tree(N, query):
    tree = SegTree(
        [nan] * (N + 1),
        take_sum,
        0,
    )
    ans = []
    for q in query:
        t, x, y, v = q
        if t == 0:
            # 交互に+/-で持っている必要があるため
            val = v if x % 2 == 0 else -v
            tree.update(x, val)
        if t == 1:
            sol = tree_query(x, y, v, tree)
            if isnan(sol):
                ans.append("Ambiguous")
            else:
                ans.append(str(sol))
    return ans


def tree_query(x, y, v, tree):
    if x < y:
        sign = 1 if x % 2 == 0 else -1
        if (y - x) % 2 == 1:
            # x_i+n = sigma(y_i) - v
            return sign * tree.query(x, y) - v
        else:
            return sign * -1 * tree.query(x, y) + v
    else:
        sign = 1 if y % 2 == 0 else -1
        if (x - y) % 2 == 1:
            return sign * tree.query(y, x) - v
        else:
            return sign * tree.query(y, x) + v


def one_query(x, y, v, checkers):
    # None の性で和が取れない場合は "Ambiguous"
    # 取れる場合は、rangeのsumで解決
    try:
        if x < y:
            sign = 1 if x % 2 == 0 else -1
            if (y - x) % 2 == 1:
                # x_i+n = sigma(y_i) - v
                return sign * sum(checkers[x:y]) - v
            else:
                return sign * -1 * sum(checkers[x:y]) + v
        else:
            sign = 1 if y % 2 == 0 else -1
            if (x - y) % 2 == 1:
                return sign * sum(checkers[y:x]) - v
            else:
                return sign * sum(checkers[y:x]) + v
    except TypeError as e:
        return "Ambiguous"


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

    def query(self, l, r):
        """
        [l, r)のsegfuncしたものを得る
        l: index(0-index)
        r: index(0-index)
        """
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


def test_one_query():
    assert one_query(1, 2, 1, [None, -3, None, None]) == 2
    assert one_query(3, 4, 5, [None, -3, None, None]) == "Ambiguous"
    assert one_query(3, 4, 5, [None, -3, None, -6]) == 1
    assert one_query(3, 1, 5, [None, -3, 6, -6]) == 2


def do_query_one(N, x, y, v, sums):
    a = [None] * (N + 1)
    a[x] = v
    # xとyが連結する場合は、値が1意に定まる -> UnionTree?
    # xから辿ってyにたどり着けるかどうか
    di = 1 if x < y else -1
    i = x
    while True:
        # 確定した場合
        if i == y:
            if a[i] is None:
                return "Ambiguous"
            else:
                return a[i]
        # 確定しない場合
        # 前進
        if di == 1:
            if sums[i] is None:
                return "Ambiguous"
            a[i + 1] = sums[i] - a[i]
            i += 1

        # 後進
        if di == -1:
            if sums[i - 1] is None:
                return "Ambiguous"
            a[i - 1] = sums[i - 1] - a[i]
            i -= 1
