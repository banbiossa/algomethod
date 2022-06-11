def test_main():
    inputs = [
        """6 7 1
1 2 3 4 5 6
""",
        """10 1 0
0 0 0 0 0 0 0 0 0 0
""",
    ]
    answers = [1, 252]
    for text, answer in zip(inputs, answers):
        N, P, Q = map(int, text.splitlines()[0].split())
        A = list(map(int, text.splitlines()[1].split()))
        assert main(N, P, Q, A) == answer
        assert ac(N, P, Q, A) == answer


from functools import reduce
from itertools import combinations


def main(N, P, Q, A):
    B = [a % P for a in A]
    # 全探索してみる
    count = 0
    for nums in combinations(B, 5):
        prod = reduce(lambda x, y: (x * y) % P, nums, 1)
        if prod % P == Q:
            count += 1
    return count


def ac(N, P, Q, A):
    count = 0
    for i in range(N):
        for j in range(i):
            for k in range(j):
                for l in range(k):
                    for m in range(l):
                        if (
                            reduce(
                                lambda x, y: (x * y) % P,
                                [A[a] for a in (i, j, k, l, m)],
                                1,
                            )
                            % P
                            == Q
                        ):
                            count += 1
    return count


def test_reduce():
    assert reduce(lambda x, y: x * y, [2, 3, 4], 1) == 24
