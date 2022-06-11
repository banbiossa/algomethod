from bisect import bisect_left, bisect_right
from itertools import accumulate


def test_main():
    inputs = [
        """3 4
1 1
2 5
7 4
""",
        """2 123
4 5
678 901
""",
        """7 10
20 20
20 20
20 30
20 40
30 20
30 30
40 20
""",
    ]
    answers = [2, 1, 5]

    for text, answer in zip(inputs, answers):
        N, K = map(int, text.splitlines()[0].split())
        query = []
        for i in range(N):
            a, b = map(int, text.splitlines()[i + 1].split())
            query.append((a, b))

        assert main(N, K, query) == answer


def main(N, K, query):
    import numpy as np


def _main(N, K, query):
    # 2次元累積和を取る
    x_max = max(i for i, j in query)
    y_max = max(j for i, j in query)
    MAX = min(5000, max(x_max, y_max)) + 1
    grid = [[0] * MAX for _ in range(MAX)]
    for a, b in query:
        grid[a][b] += 1

    # 行方向の cumsum
    row_sum = [list(accumulate(row)) for row in grid]

    # 列方向にさらに sum
    col_sum = [list(accumulate(row_sum[i][j] for i in range(MAX))) for j in range(MAX)]

    # 転地してcumsumになる
    cum_sum = [[col_sum[j][i] for j in range(MAX)] for i in range(MAX)]

    # i, j range(5000), range(5000) に対して
    p_grid = [[0] * MAX for _ in range(MAX)]
    for i in range(1, MAX):
        for j in range(1, MAX):
            try:
                p_grid[i][j] = (
                    cum_sum[i - 1][j - 1]
                    + cum_sum[i + K][j + K]
                    - cum_sum[i - 1][j + K]
                    - cum_sum[i + K][j - 1]
                )
            except Exception:
                continue
    # Prx,ry - Plx-1,ry - Prx,ly-1 + Plx-1,ly-1 を計算
    # その max を返す
    return max(max(row) for row in p_grid)


def main__(N, K, query):
    # coords = [(i, q[0], q[1]) for i, q in enumerate(query)]

    # 1次元目でsort
    coord_1 = [(i, q[0]) for i, q in enumerate(query)]
    sort_1 = sorted(coord_1, key=lambda x: x[1])
    keys_1 = [i[1] for i in sort_1]

    # 2次元目でsort
    coord_2 = [(i, q[1]) for i, q in enumerate(query)]
    sort_2 = sorted(coord_2, key=lambda x: x[1])
    keys_2 = [i[1] for i in sort_2]

    max_points = 0

    # 片方から iterate
    for index in range(N):
        # index = 0

        #   0: bisect して index を出す
        minimum = coord_1[index][1]
        to_find = minimum + K
        start_point = bisect_left(keys_1, minimum)
        insertion_point = bisect_right(keys_1, to_find)
        from_0 = {i for (i, _) in sort_1[start_point:insertion_point]}

        #   1: bisect して index を出す
        minimum = coord_2[index][1]
        to_find = minimum + K
        start_point = bisect_left(keys_2, minimum)
        insertion_point = bisect_right(keys_2, to_find)
        from_1 = {i for (i, _) in sort_2[start_point:insertion_point]}

        #   set を取る
        common = from_0 & from_1
        max_points = max(max_points, len(common))

    return max_points


def main_(N, K, query):
    coords = [(i, q[0], q[1]) for i, q in enumerate(query)]

    # 1次元目でsort
    sort_1 = sorted(coords, key=lambda x: x[1])

    # 2次元目でsort
    sort_2 = sorted(coords, key=lambda x: x[2])

    max_points = 0

    # 片方から iterate
    for index in range(N):
        # index = 0

        #   0: bisect して index を出す
        minimum = sort_1[index][1]
        to_find = minimum + K
        insertion_point = bisect_right(sort_1, to_find, key=lambda x: x[1])
        from_0 = {i for (i, _, _) in sort_1[index:insertion_point]}

        #   1: bisect して index を出す
        minimum = sort_1[index][2]
        to_find = minimum + K
        start_point = bisect_left(sort_2, minimum, key=lambda x: x[2])
        insertion_point = bisect_right(sort_2, to_find, key=lambda x: x[2])
        from_1 = {i for (i, _, _) in sort_2[start_point:insertion_point]}

        #   set を取る
        common = from_0 & from_1
        max_points = max(max_points, len(common))

    return max_points
