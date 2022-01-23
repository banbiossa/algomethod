def test_main():
    inputs = [
        """2
1 2
1 2
""",
        """3
3 3
1 1
4 4
""",
        """3
1 10
38 40
8 87""",
        """4
1 10
38 40
8 87
2 9""",
        """10
1 10
38 40
8 87
2 9
75 100
45 50
89 92
27 77
23 88
62 81
""",
    ]
    answers = [
        "0.250000000000",
        "1.000000000000",
        "0.39125",
        "2.8365625",
        "13.696758921226",
    ]
    count = 0
    for text, answer in zip(inputs, answers):
        # if count > 3:
        #     break
        count += 1
        N = int(text.splitlines()[0])
        query = []
        for i in range(N):
            L, R = map(int, text.splitlines()[i + 1].split())
            query.append((L, R))

        assert abs(main(N, query) - float(answer)) < 1e-7


def main(N, query):
    # 各ペアごとに、inversionする場合を足していく
    # print(N, query)
    # denominator = prod([(q[1] - q[0] + 1) for q in query])
    ratio = 0
    for i, j in itertools.combinations(range(N), 2):
        ratio += inversions_count(query[i], query[j])
    return ratio


def inversions_count(a, b):
    denominator = (a[1] - a[0] + 1) * (b[1] - b[0] + 1)
    count = 0
    for i in range(a[0], a[1] + 1):
        for j in range(b[0], b[1] + 1):
            if i > j:
                count += 1
    return count / denominator


def inversions(a, b):
    denominator = (a[1] - a[0] + 1) * (b[1] - b[0] + 1)

    # 被りがない場合
    if a[1] <= b[0]:
        return 0
    # フルでずれる場合
    if b[1] <= a[0]:
        return 1

    total = 0
    # 被り部分は n(n-1)/2
    n0 = max(a[0], b[0])
    n1 = min(a[1], b[1])
    n = n1 - n0
    if n > 0:
        total += n * (n + 1) // 2

    # 左のずれ
    if b[0] < a[0]:
        total += (a[1] - a[0] + 1) * (a[0] - b[0])

    # 右のずれ
    if a[1] > b[1] and n >= 0:
        total += (n + 1) * (a[1] - b[1])

    # かける
    return total / denominator


import itertools
from math import prod


def full_search(N, query):
    ranges = [range(q[0], q[1] + 1) for q in query]
    numerator = 0
    for nums in itertools.product(*ranges):
        numerator += inversion_number(N, nums)

    denominator = prod([(q[1] - q[0] + 1) for q in query])

    return numerator / denominator


def inversion_number(N, nums):
    count = 0
    for i in range(N - 1):
        for j in range(i + 1, N):
            if nums[i] > nums[j]:
                count += 1
    return count


def test_inversion_number():
    assert inversion_number(3, [1, 2, 3]) == 0
    assert inversion_number(3, [3, 2, 3]) == 1
    assert inversion_number(3, [3, 2, 1]) == 3
