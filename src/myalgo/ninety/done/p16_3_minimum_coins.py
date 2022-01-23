def test_main():
    inputs = [
        """227
21 47 56
""",
        """9999
1 5 10
""",
        """998244353
314159 265358 97932
""",
        """100000000
10001 10002 10003
""",
    ]
    answers = [5, 1004, 3333, 9998]
    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        A, B, C = map(int, text.splitlines()[1].split())
        assert main(N, A, B, C) == answer


def gcd(A, B):
    if B == 0:
        return A
    return gcd(B, A % B)


def lcm(A, B):
    return A * (B // gcd(A, B))


def lcmn(N, *nums):
    # 最小公倍数を作る。Nより大きくなるなら None か -1 か？
    product = 1
    for i in range(len(nums) - 1):
        a = nums[i]
        b = nums[i + 1]
        product *= lcm(a, b)
        if product > N:
            return None
    return product


def test_lcmn():
    assert lcmn(100, 2, 3) == 6
    assert lcmn(1, 2, 3) is None


def _main(N, *nums):
    # a < b < c
    a, b, c = sorted(nums)

    factors = [
        ("a", a),
        ("b", b),
        ("c", c),
        ("ab", lcmn(N, a, b)),
        ("bc", lcmn(N, b, c)),
        ("ca", lcmn(N, c, a)),
        ("abc", lcmn(N, a, b, c)),
    ]
    factor_dict = {a: b for a, b in factors}
    # 3つの数の lcm で減らし続けたい
    if factor_dict["abc"] is not None:
        N %= factor_dict["abc"]
    print(N)


def main_bad(N, a, b, c):
    ans = 9999
    L = 9999
    for x in range(L):
        for y in range(L):
            for z in range(L):
                if a * x + b * y + c * z == N:
                    ans = min(ans, x + y + z)
    return ans


def main(N, a, b, c):
    ans = 9999
    L = 9999
    for x in range(min(L, N // a) + 1):
        for y in range(min(L, (N - a * x) // b) + 1):
            z = (N - a * x - b * y) // c
            if z < 0:
                continue
            if a * x + b * y + c * z == N:
                ans = min(ans, x + y + z)
    return ans
