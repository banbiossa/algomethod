def main(N):
    ans = []
    # 奇数なら何もなし
    if N % 2 != 0:
        return ans
    # from largest 1 is (, 0 is )
    for i in range(2 ** N, 0, -1):
        b = as_binary(i, N)
        if is_ok(b, N):
            ans.append(to_paren(b))
    return ans


def to_paren(b):
    return b.replace("1", "(").replace("0", ")")


def test_to_paren():
    assert to_paren("1100") == "(())"
    assert to_paren("1010") == "()()"


def is_ok(b, N):
    if b.count("1") != N // 2:
        return False
    count = 0
    for c in b:
        if c == "1":
            count += 1
        else:
            count -= 1
        if count < 0:
            return False
    return True


def test_is_ok():
    assert not is_ok("1110", 4)
    assert not is_ok("1001", 4)
    assert is_ok("1010", 4)


def as_binary(n, digits):
    return bin(n)[2:].zfill(digits)


def test_as_binary():
    assert as_binary(4, 4) == "0100"
    assert as_binary(4, 8) == "00000100"


def pprint(ans):
    for a in ans:
        print(a)


def test_main():
    inputs = [2, 3, 4, 10]
    outputs = [
        "()",
        "",
        """(())
        ()()
        """,
        """((((()))))
    (((()())))
    (((())()))
    (((()))())
    (((())))()
    ((()(())))
    ((()()()))
    ((()())())
    ((()()))()
    ((())(()))
    ((())()())
    ((())())()
    ((()))(())
    ((()))()()
    (()((())))
    (()(()()))
    (()(())())
    (()(()))()
    (()()(()))
    (()()()())
    (()()())()
    (()())(())
    (()())()()
    (())((()))
    (())(()())
    (())(())()
    (())()(())
    (())()()()
    ()(((())))
    ()((()()))
    ()((())())
    ()((()))()
    ()(()(()))
    ()(()()())
    ()(()())()
    ()(())(())
    ()(())()()
    ()()((()))
    ()()(()())
    ()()(())()
    ()()()(())
    ()()()()()
    """,
    ]

    for N, answer in zip(inputs, outputs):
        as_list = answer.split()
        assert main(N) == as_list
