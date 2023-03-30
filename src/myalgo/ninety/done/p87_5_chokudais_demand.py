"""問題
- N 個の国
- A[i,j] == -1 -> A[i,j]
- A[i,j] == -1 -> X
- i からj まで P以下で到達可能な(i,j)がK組存在する

- X の選び方はいくつあるか
"""

"""方針
Xの時 n組、が言えれば二部探索できそう

"""


def main(N, P, K, A):
    """
    N: int number of countries <= 40
    P: int total cost <= 10**9
    K: int number of pairs that should exist <= N(N-1)/2
    A: matrix of cost between countries
    """
    # lower bound を求める二部探索と、upper bound を求める二部探索を行う
    # 答えは、upper bound - lower bound + 1
    # 二部探索, 範囲は0からX+1, X+1 は無限大

    # find the lower bound (the first time that the condition is satisfied)
    # or the last time res == K-1 is satisfied

    if warshall_floyd(A, P + 1, P) == K:
        return "Infinity"

    min_cost_for_k = binary_search(A, P, K)
    # min_cost_for_k_plus_1 = binary_search(A, P, K + 1)
    min_cost_for_k_minus_1 = binary_search(A, P, K - 1, left=min_cost_for_k - 1)

    # if min_cost_for_k == P + 1:
    #     if min_cost_for_k_plus_1 == P + 1:
    #         return 0
    #     else:
    #         return "Infinity"
    return min_cost_for_k_minus_1 - min_cost_for_k
    # return min_cost_for_k - min_cost_for_k_plus_1


def binary_search(A, P, k, left=0):
    # find the maximum x that has k paths less than P
    # if P + 1 is returned, it means that any x is OK
    # right を返す
    # left = 0
    right = P + 1
    if warshall_floyd(A, right, P) > k:
        return 0

    while right - left > 1:
        mid = (left + right) // 2
        # res = dykstra_all(A, mid, P)
        if warshall_floyd(A, mid, P) <= k:
            right = mid
        else:
            left = mid
    return right


def warshall_floyd(A, x, P):
    N = len(A)
    dist = [[float("inf")] * N for _ in range(N)]
    # init
    for i in range(N):
        for j in range(N):
            if A[i][j] == -1:
                dist[i][j] = x
            else:
                dist[i][j] = A[i][j]
        dist[i][i] = 0

    # update
    for k in range(N):
        for i in range(N):
            for j in range(N):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    # count where dist[i][j] <= P
    return sum([1 for i in range(N) for j in range(i + 1, N) if dist[i][j] <= P])


def dykstra(A, x, i, j, P) -> int:
    # コストをxとした時に、i から j までの最短経路を求める
    # returns if cost is less than P
    A = A.copy()
    A = get_new_A(A, x)
    N = len(A)

    # initialize
    dist = [float("inf")] * N
    dist[i] = 0
    used = [False] * N

    while True:
        v = -1
        for u in range(N):
            if not used[u] and (v == -1 or dist[u] < dist[v]):
                v = u
        if v == -1:
            break
        used[v] = True
        for u in range(N):
            dist[u] = min(dist[u], dist[v] + A[v][u])

    return dist[j] <= P


def dykstra_all(A, x, P) -> int:
    # 全てのi,jの組について、dykstraを行う
    # P 以下の経路の数の和を返す
    total = 0
    N = len(A)
    for i in range(N):
        for j in range(i + 1, N):
            if dykstra(A, x, i, j, P):
                total += 1
    return total


def get_new_A(A, x):
    A = A.copy()
    new_A = []
    N = len(A)
    for i in range(N):
        new_A.append([])
        for j in range(N):
            if A[i][j] == -1:
                new_A[i].append(x)
            else:
                new_A[i].append(A[i][j])
    return new_A


def test_get_new_A():
    A = [
        [0, 3, -1],
        [3, 0, 5],
        [-1, 5, 0],
    ]
    x = 10
    expected = [
        [0, 3, 10],
        [3, 0, 5],
        [10, 5, 0],
    ]
    actual = get_new_A(A, x)
    assert actual == expected


def test_main():
    inputs = [
        """3 4 2
    0 3 -1
    3 0 5
    -1 5 0
    """,
        """3 10 2
0 -1 10
-1 0 1
10 1 0
""",
        """13 777 77
0 425 886 764 736 -1 692 660 -1 316 424 490 423
425 0 -1 473 -1 311 -1 -1 903 941 386 521 486
886 -1 0 605 519 473 775 467 677 769 690 483 501
764 473 605 0 424 454 474 408 421 530 756 568 685
736 -1 519 424 0 -1 804 598 911 731 837 459 610
-1 311 473 454 -1 0 479 613 880 -1 393 875 334
692 -1 775 474 804 479 0 579 -1 -1 575 985 603
660 -1 467 408 598 613 579 0 456 378 887 -1 372
-1 903 677 421 911 880 -1 456 0 859 701 476 370
316 941 769 530 731 -1 -1 378 859 0 800 870 740
424 386 690 756 837 393 575 887 701 800 0 -1 304
490 521 483 568 459 875 985 -1 476 870 -1 0 716
423 486 501 685 610 334 603 372 370 740 304 716 0""",
    ]
    answers = [
        3,
        "Infinity",
        42,
    ]
    for test_input, expected in zip(inputs, answers):
        N, P, K = map(int, test_input.split("\n")[0].split())
        A = []
        for i in range(N):
            A.append(list(map(int, test_input.split("\n")[i + 1].split())))
        actual = main(N, P, K, A)
        assert actual == expected


if __name__ == "__main__":
    # code to parse
    N, P, K = map(int, input().split())
    A = []
    for i in range(N):
        A.append(list(map(int, input().split())))
    print(main(N, P, K, A))
