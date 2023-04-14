"""
N個のボールがある
どの2つを選んでも、書かれている整数の差がk以上である選び方
N行のアウトプットになる

うーんなんかの漸化式ぽいけど
"""

BIG = 10**9 + 7


class N_C_R:
    def __init__(self, big_n):
        self.mod = 10**9 + 7

        self.fact = factorial(big_n)

    def __call__(self, n, r):
        if r < 0 or n < r:
            return 0
        # n_C_r = n! / (r! * (n-r)!)
        nominator = self.fact[n]

        r_factorial = self.fact[r]
        n_minus_r_factorial = self.fact[n - r]
        denominator = (r_factorial * n_minus_r_factorial) % BIG

        # n! / denominator を逆元から求める
        return moddiv(nominator, denominator)


def main(N):
    # the point is to do this initialization only once
    n_c_r = N_C_R(N)
    answer = []
    for k in range(N):
        answer.append(how_many(n_c_r, N, k + 1))
    return answer


def how_many(n_c_r, n, k):
    # 選び方は N-(k-1)(a-1) C a 通り
    # n C r は逆元を用いて高速に計算する？
    total = 0
    for a in range(1, n + 1):
        num = n_c_r(n - (k - 1) * (a - 1), a)
        if num == 0:
            break
        total = (total + num) % BIG
    return total


# def n_c_r(n, r):
#     if r < 0 or n < r:
#         return 0
#
#     # n_C_r = n! / (r! * (n-r)!)
#     fact = factorial2(n)
#
#     # return (fact[n] * pow(fact[r] * fact[n - r], BIG - 2, BIG)) % BIG
#     nominator = fact[n]
#
#     r_factorial = fact[r]
#     n_minus_r_factorial = fact[n - r]
#     denominator = (r_factorial * n_minus_r_factorial) % BIG
#
#     # n! / denominator を逆元から求める
#     return moddiv(nominator, denominator)


# def test_ncr():
#     assert n_c_r(3, 1) == 3
#     assert n_c_r(3, 2) == 3
#     assert n_c_r(4, 2) == 6
#     assert n_c_r(10, 2) == 45
#


def moddiv(a, b):
    # a/bを逆元を求める
    return (a * pow(b, BIG - 2, BIG)) % BIG


def test_moddiv():
    assert moddiv(1, 2) == 500000004


def factorial2(n):
    arr = [1] * (n + 1)
    for i in range(1, n + 1):
        arr[i] = (arr[i - 1] * i) % BIG
    return arr


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
    res = main(n)
    for ans in res:
        print(ans)
