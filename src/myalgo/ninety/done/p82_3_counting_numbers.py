def test_main():
    inputs = ["3 5", "98 100", "1001 869120", "381453331666495446 746254773042091083"]
    answers = [
        12,
        694,
        59367733,
        584127830,
    ]
    for text, answer in zip(inputs, answers):
        L, R = map(int, text.split())
        m = main(L, R)
        assert main(L, R) == answer
        if m != answer:
            print(m, answer)


def simple(L, R, n):
    BIG = 10 ** 9 + 7
    assert len(str(L)) == len(str(R)) == n
    a = (L + R) % BIG * (R - L + 1) % BIG * n % BIG
    b = 2
    # これを2で割りたいので、逆元を求める
    return revmod(a, b)


def modinv(b, mod=10 ** 9 + 7):
    return pow(b, mod - 2, mod)


def revmod(a, b):
    # a / b -> b*t === a (mod p)
    # t = a * b ** (p-2) (mod p)
    p = 10 ** 9 + 7
    return a * modinv(b) % p


def test_revmod():
    assert revmod(678813585, 100000) == 123456789


def test_simple():
    assert simple(3, 5, 1) == 12


def main(L, R):
    BIG = 10 ** 9 + 7
    total = 0
    for i in range(len(str(L)), len(str(R)) + 1):
        if len(str(L)) < i:
            l = 10 ** (i - 1)
        else:
            l = L
        if len(str(R)) > i:
            r = 10 ** i - 1
        else:
            r = R
        add = simple(l, r, i)
        total += add
        total %= BIG
    return total
