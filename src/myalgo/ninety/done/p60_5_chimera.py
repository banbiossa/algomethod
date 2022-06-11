def test_main():
    inputs = [
        """6
1 2 3 3 2 1
""",
        """4
1 2 3 4
""",
        """5
3 3 3 3 3
""",
    ]
    answers = [5, 4, 1]
    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        A = list(map(int, text.splitlines()[1].split()))
        assert main(N, A) == answer
        assert ac(N, A) == answer
        assert try2(N, A) == answer


from bisect import bisect_left


def try2(N, A):
    p = lis_length(N, A)
    q = lis_length(N, A[::-1])[::-1]
    best = 0
    for i in range(N):
        best = max(best, p[i] + q[i] - 1)
    return best


def lis_length(N, A):
    # https://qiita.com/python_walker/items/d1e2be789f6e7a0851e5
    res = [0] * N
    res[0] = 1
    ans = [A[0]]
    for i in range(1, N):
        if A[i] > ans[-1]:
            ans.append(A[i])
        else:
            index = bisect_left(ans, A[i])
            ans[index] = A[i]
        res[i] = len(ans)
    return res


def test_lis_length():
    assert lis_length(6, [1, 3, 5, 2, 1, 4]) == [1, 2, 3, 3, 3, 3]


def ac(N, A):
    p = lis(N, A)
    q = lis(N, A[::-1])
    best = 0
    for k in set(p) | set(q):
        p_val = p.index(k) if k in p else 0
        q_val = q.index(k) if k in q else 0
        current = p_val + q_val + 1
        best = max(best, current)
    return best


def lis(N, A):
    # https://qiita.com/python_walker/items/d1e2be789f6e7a0851e5
    ans = [A[0]]
    for i in range(1, N):
        if A[i] > ans[-1]:
            ans.append(A[i])
        else:
            index = bisect_left(ans, A[i])
            ans[index] = A[i]
    return ans


def test_lis():
    assert lis(6, [1, 3, 5, 2, 1, 4]) == [1, 2, 4]


def LIS(x):
    N = len(x)
    res = [0] * N
    now = [-1]
    for i in range(N):
        j = bisect_left(now, x[i])
        res[i] = j
        if j == len(now):
            now.append(x[i])
        else:
            now[j] = x[i]
    return res


def test_LIS():
    assert LIS([1, 3, 5, 2, 1, 4]) == [1, 2, 3, 2, 1, 3]


def LISSample(sample):
    inf = 10**10
    res = []
    K = len(sample)
    L = [inf] * (len(sample) + 1)
    t = 0
    for i, s in enumerate(sample):
        index = bisect_left(L, s)  # 重複なし(狭義)
        L[index] = s
        res.append(L[i])
        for t in range(t, K + 1):
            if L[t] == inf:
                break
        res[i] = t
    return res


def test_LISSample():
    assert LISSample([1, 3, 5, 2, 1, 4]) == [1, 2, 3, 3, 3, 3]


def main(N, A):
    # 単調増加な部分列を左右から作って、いい感じに合体させる
    # 作り方はdp(N*N) 自分を使う場合/使わない場合の長さと最大値を持つ
    # 使う場合は更新するときに自分の値で上書きする
    # 1, 2, 3, 5, 4, 3, 6, 2, 1
    # 1,2,3,5,6,2,1
    # 1,2,3,5,4,3,2,1

    # 1,2,3,5,6,2,1
    one = find_mono_increase(N, A)
    two = find_mono_increase(N, A[::-1])
    current = 0
    for j in range(N + 1):
        # j文字目までを左から使う
        left = [one[i][j] for i in range(N)]
        right = [two[i][N - j] for i in range(N)]
        max_l = nanmax(*left)
        len_l = left.index(max_l)
        max_r = nanmax(*right)
        len_r = right.index(max_r)
        if max_l == max_r:
            best = len_l + len_r - 1
        else:
            best = len_l + len_r
        current = max(best, current)
    return current


def test_min():
    assert nanmin(3, None) == 3


def test_nanmax():
    assert nanmax(3, 4, 5, None) == 5
    assert nanmax() == 0


def nanmax(*args):
    if len(args) == 0:
        return 0
    return max([i for i in args if i is not None])


def nanmin(a, b):
    return min([i for i in (a, b) if i is not None])


def find_mono_increase(N, A):
    dp = [[None] * (N + 1) for _ in range(N + 1)]
    # dp[i][j] 長さiの文字を作ったときに、j文字目までを使った場合の最大値
    dp[0][0] = 0

    # 行方向
    for i in range(N):
        # 列方向
        for j in range(N):
            if dp[i][j] is None:
                continue
            # 自分を使わない場合
            dp[i][j + 1] = dp[i][j]
            # 自分を使った場合

            # シンプルな場合: lastより自分が大きく、lengthが短い
            # 複雑な場合: lastより自分が小さく、lengthが短い
            # 同じ長さを達成するのに最適なのか？
            # 1, 3, 5, 2, 3, 4, 2, 3
            if A[j] > dp[i][j]:
                dp[i + 1][j + 1] = nanmin(A[j], dp[i + 1][j + 1])

    return dp

    # for i in range(N, 0, -1):
    #     if dp[i][-1] is not None:
    #         return dp[N][-1]
