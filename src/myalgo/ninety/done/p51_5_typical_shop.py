from collections import defaultdict
from bisect import bisect_right


def test_main():
    inputs = [
        """5 2 10
3 8 7 5 11
""",
        """5 1 10
7 7 7 7 7
""",
        """40 20 100
1 3 1 3 4 1 3 5 5 3 3 4 1 5 4 4 3 1 3 4 1 3 2 4 4 1 5 2 5 3 1 3 3 3 5 5 5 2 3 5
""",
    ]
    answers = [2, 5, 137846528820]

    for text, answer in zip(inputs, answers):
        N, K, P = map(int, text.splitlines()[0].split())
        A = list(map(int, text.splitlines()[1].split()))
        assert main(N, K, P, A) == answer


def main(N, K, P, A):
    one = A[: N // 2]
    two = A[N // 2 :]

    first = describe_all(one, K)
    second = describe_all(two, K)

    total = 0
    for k1, l1 in first.items():
        k2 = K - k1
        l2 = second[k2]
        # N-v1以下の値を見つける
        for v in l1:
            total += bisect_right(l2, P - v)
    return total


def describe_all(A, K):
    # 全列挙する
    N = len(A)
    d = defaultdict(list)
    # binary 全探索
    for i in range(2 ** N):
        key = bin(i).count("1")
        if key > K:
            continue
        value = sum([A[j] for j in range(N) if i & (1 << j)])
        d[key].append(value)

    for v in d.values():
        v.sort()

    return d
