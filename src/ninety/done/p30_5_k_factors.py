def test_main():
    inputs = ["15 2", "30 2", "200 4", "869120 1", "10000000 3"]
    answers = [5, 13, 0, 869119, 6798027]

    for text, answer in zip(inputs, answers):
        N, K = map(int, text.split())
        # assert main(N, K) == answer
        # assert len(brute_force(N, K)) == answer
        # assert with_dp(N, K) == answer
        # assert ac(N, K) == answer
        assert Eratosthenes(N, K) == answer


def ac(N, K):
    dp = [0] * (N + 1)
    ps = primes(N)
    for p in ps:
        for j in range(p, N + 1, p):
            dp[j] += 1
    more_than_k = [i for i in dp if i >= K]
    return len(more_than_k)


def main(N, K):
    if K == 1:
        # 1以外なので
        return N - 1
    ps = primes(N)
    if K == 2:
        return N - len(ps) - 1


def with_dp(N, K):
    # dp でやってみる
    dp = [(n, 0) for n in range(N + 1)]
    ps = primes(N)
    for p in ps:
        for i, (n, c) in enumerate(dp):
            if n == 0 or n == 1 or n % p != 0:
                continue
            while n % p == 0:
                n //= p
            dp[i] = (n, c + 1)
    # filter
    good = [(n, c) for n, c in dp if c >= K]
    return len(good)


# 1 以上 N 以下の整数が素数かどうかを返す
def Eratosthenes(N, K):
    # テーブル
    isprime = [True] * (N + 1)
    dp = [0] * (N + 1)

    # 0, 1 は予めふるい落としておく
    isprime[0], isprime[1] = False, False

    # ふるい
    for p in range(2, N + 1):
        # すでに合成数であるものはスキップする
        if not isprime[p]:
            continue
        dp[p] += 1

        # p 以外の p の倍数から素数ラベルを剥奪
        q = p * 2
        while q <= N:
            isprime[q] = False
            dp[q] += 1
            q += p

    # 1 以上 N 以下の整数が素数かどうか
    good = [i for i in dp if i >= K]
    return len(good)


def primes(N):
    # Nまでの素数
    sieve = list(range(2, N + 1))
    res = []
    p = 2
    while True:
        for num in sieve:
            if num % p == 0:
                sieve.remove(num)
        res.append(p)
        if len(sieve) == 0:
            break
        p = sieve[0]
    return res


def test_primes():
    assert primes(2) == [2]
    assert primes(13) == [2, 3, 5, 7, 11, 13]
    assert primes(25) == [2, 3, 5, 7, 11, 13, 17, 19, 23]


def brute_force(N, K):
    # 1-N までの全ての数に対して、prime_factorizeしてK以上か判定する
    ans = []
    for i in range(1, N + 1):
        if len(prime_factorize(i)) >= K:
            ans.append(i)
    return ans


def prime_factorize(n):
    ans = set()
    p = 2
    while n > 1:
        while n % p == 0:
            ans.add(p)
            n //= p
        p += 1
    return ans


def test_prime_factorize():
    assert prime_factorize(8) == {2}
    assert prime_factorize(21) == {3, 7}
