"""
N個のボールがある
どの2つを選んでも、書かれている整数の差がk以上である選び方
N行のアウトプットになる

うーんなんかの漸化式ぽいけど
"""

BIG = 10**9 + 7


def main(N):
    answer = []
    for k in range(N):
        # answer.append(f(N, k + 1))
        answer.append(how_many(N, k + 1))
    return answer


def how_many(n, k):
    # 選び方は N-(k-1)(a-1) C a 通り
    # n C r は逆元を用いて高速に計算する？

    # for a in range(1, (n // k) + 1):
    #     total += n_c_r(n - (k - 1) * (a - 1), a)
    #     total %= BIG

    total = 0
    a = 1
    while n - (k - 1) * (a - 1) >= a:
        total += n_c_r(n - (k - 1) * (a - 1), a)
        total %= BIG
        a += 1
    return total


def n_c_r(n, r):
    if n <= 0 or r <= 0 or n < r:
        return 0
    # n_C_r = n! / (r! * (n-r)!)
    fact = factorial(n)
    nominator = fact[n]

    r_factorial = fact[r]
    n_minus_r_factorial = fact[n - r]
    denominator = (r_factorial * n_minus_r_factorial) % BIG

    # n! / denominator を逆元から求める
    return moddiv(nominator, denominator)


def test_ncr():
    assert n_c_r(3, 1) == 3
    assert n_c_r(3, 2) == 3
    assert n_c_r(4, 2) == 6
    assert n_c_r(10, 2) == 45


def moddiv(a, b):
    # a/bを逆元を求める
    return (a * pow(b, BIG - 2, BIG)) % BIG


def test_moddiv():
    assert moddiv(1, 2) == 500000004


def modpow2(a, k):
    return pow(a, k, BIG)


def modpow(a, k):
    # a ** k at mod BIG
    p = 1
    q = a
    for i in range(32):
        if k & (1 << i):
            p *= q
            p %= BIG
        q *= q
        q %= BIG

    return p


def test_modpow():
    assert modpow(3, 2) == 9
    assert modpow(3, 3) == 27


def factorial(n):
    arr = [1]
    total = 1
    for i in range(1, n + 1):
        total = (total * i) % BIG
        arr.append(total)
    return arr


def test_factorial():
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24


# def main(N):
#     # less memory
#     for k in range(N):
#         print(f(N, k + 1))


def fibonacci_sum(n):
    # make a fibonacci sequence, and sum it
    if n == 0:
        return 0
    if n == 1:
        return 0

    BIG = 10**9 + 7
    fib = [1, 1]

    for i in range(2, n):
        fib.append((fib[i - 1] + fib[i - 2]) % BIG)
    total = 0
    for num in fib:
        total = (total + num) % BIG
    return total


def f(n, k):
    """
    the array[i] can be calculated as the following
    - 1 up to i=k
    - arr[i] = 1 + sum(arr[1] + ... + arr[i-k])

    this can be slightly simplified as
    - 1 up to i=k
    - arr[i] = arr[i-1] + arr[i-k]

    the sum of the array (length n) is the final answer.

    this can be tested by the following:
    f(n, 1) == 2 ** (n-1)
    f(n, 2) == fibonacci_sum(n)
    (for others try the test cases)
    """
    BIG = 10**9 + 7

    arr = []
    for i in range(k):
        arr.append(1)
    for i in range(k, n):
        arr.append((arr[i - 1] + arr[i - k]) % BIG)

    # take sum
    total = 0
    for num in arr:
        total = (total + num) % BIG
    return total


def test_f():
    assert f(3, 1) == 2**3 - 1
    assert f(10, 1) == 2**10 - 1

    assert f(3, 2) == fibonacci_sum(3)
    assert f(10, 2) == fibonacci_sum(10)


def test_fibonacci_sum():
    assert fibonacci_sum(2) == 2
    assert fibonacci_sum(4) == 7
    assert fibonacci_sum(7) == 33
    assert fibonacci_sum(20) == 17710
    assert fibonacci_sum(50) == 951279874
    large = fibonacci_sum(10**5)
    print(large)


def test_main():
    inputs = [
        1,
        2,
        3,
        4,
        7,
        20,
        50,
    ]
    answers = [
        "1",
        """3
2
""",
        """7
4
3
""",
        """15
7
5
4
""",
        """127
33
18
13
10
8
7
""",
        """1048575
17710
2744
906
430
250
167
118
90
75
65
56
48
41
35
30
26
23
21
20
""",
        """898961330
951279874
262271567
14341526
1985602
466851
153365
63191
30623
16687
9987
6453
4354
3070
2290
1790
1427
1138
910
735
605
512
448
405
375
350
326
303
281
260
240
221
203
186
170
155
141
128
116
105
95
86
78
71
65
60
56
53
51
50
""",
    ]

    for n, expected in zip(inputs, answers):
        actual = main(n)
        expected = list(map(int, expected.splitlines()))
        assert actual == expected


if __name__ == "__main__":
    n = int(input())
    actual = main(n)
    # print one item each on a new line
    for a in actual:
        print(a)
