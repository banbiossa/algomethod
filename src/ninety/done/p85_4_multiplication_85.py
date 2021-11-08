def prime_factor_decomposition(N):
    ans = []
    for p in range(2, N):
        if p * p > N:
            break
        while N % p == 0:
            ans.append(p)
            N //= p
    if N != 1:
        ans.append(N)
    return ans


def test_prime_factor_decomposition():
    assert prime_factor_decomposition(5) == [5]
    assert prime_factor_decomposition(8) == [2, 2, 2]
    assert prime_factor_decomposition(24) == [2, 2, 2, 3]


def bunkai(n):
    # put 3 as 1, 1, 1
    # put 4 as 1, 1, 2
    ans = []
    for i in range(0, n):
        for j in range(i, n - i):
            k = n - i - j
            if k >= j:
                ans.append((i, j, k))
    assert len(ans) == len(set(ans))
    return ans


def to_lengths(n):
    ans = bunkai(n)
    return Counter([len(set(a)) for a in ans])


def test_to_lengths():
    b = to_lengths(10)
    assert len(b) == 2


def test_bunkai():
    a = bunkai(3)
    assert len(a) == 3
    a = bunkai(4)
    assert len(a) == 4
    a = bunkai(10)
    assert len(a) == 14


from collections import Counter, defaultdict


def mul(c, n):
    return Counter({k: v * n for k, v in c.items()})


def test_mul():
    a = Counter({3: 5})
    b = mul(a, 2)
    assert b == Counter({3: 10})


def test_counter():
    a = Counter({3: 5})
    b = Counter({3: 6})
    c = a + b
    print(c)
    d = 10 * c
    print(d)

    # 素因数分解した後の3つの数の分類方法はかなり限られる
    d = {
        (3, 3): [(3, 6)],
        (3, 2): [(3, 3)],
        (2, 2): [(3, 1), (2, 1)],
        (3, 1): [(3, 1)],
        (2, 1): [(2, 1)],
        (1, 1): [(1, 1)],
    }
    d_counter = {k: Counter({i[0]: i[1] for i in v}) for k, v in d.items()}
    print(d_counter)

    d_counter = {}
    for k, v in d.items():
        d_counter[k] = Counter({i[0]: i[1] for i in v})
        if k[0] != k[1]:
            d_counter[(k[1], k[0])] = d_counter[k]
    print(d_counter)


def main(K):
    if K == 1:
        return 1
    # 素因数分解はとりあえず必要そう
    factors = prime_factor_decomposition(K)

    # 素因数分解した後の3つの数の分類方法はかなり限られる
    d = {
        (3, 3): [(3, 6)],
        (3, 2): [(3, 3)],
        (2, 2): [(3, 1), (2, 1)],
        (3, 1): [(3, 1)],
        (2, 1): [(2, 1)],
        (1, 1): [(1, 1)],
    }
    d_counter = {}
    for k, v in d.items():
        d_counter[k] = Counter({i[0]: i[1] for i in v})
        if k[0] != k[1]:
            d_counter[(k[1], k[0])] = d_counter[k]
    # d_counter = {k: Counter({i[0]: i[1] for i in v}) for k, v in d.items()}

    # これを各素因数順にかけて和を取る？
    num_factors = []
    c = Counter(factors)
    for i, v in c.items():
        num_factors.append(to_lengths(v))

    result = Counter()
    for f in num_factors:
        if len(result) == 0:
            result += f
            continue
        tmp = Counter()
        for k1, v1 in f.items():
            for k2, v2 in result.items():
                tmp += mul(d_counter[(k1, k2)], v1 * v2)
        result = tmp

    total = sum(v for k, v in result.items())
    return total


def test_main():
    inputs = [42, 7, 192, 1]
    answers = [5, 1, 16, 1]

    for K, answer in zip(inputs, answers):
        assert main(K) == answer
