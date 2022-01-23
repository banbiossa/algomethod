def test_main():
    inputs = [
        1,
        234,
    ]
    answers = [0, 757186539]
    for K, answer in zip(inputs, answers):
        # assert main(K) == answer
        assert ac(K) == answer


def ac(K):
    if K % 9 != 0:
        return 0
    BIG = 10 ** 9 + 7
    dp = [0] * (K + 1)
    dp[0] = 1
    for i in range(1, K + 1):
        b = min(i, 9)
        for j in range(1, b + 1):
            dp[i] += dp[i - j]
            dp[i] %= BIG
    return dp[K]


def main(K):
    # x is multiple of 9
    # sum of each digit is K

    # K 自体が9の倍数でない場合は0
    if K % 9 != 0:
        return 0

    # 数字のリストが作れれば、その桁数の組み合わせ通り存在する
    # [9, 9, 9, 9] -> 4!/4!

    # リストの作り方
    # make_nums([current], left) 的な？
    # 最後の１桁より小さい数しか選べないようにすることで、被りなく出せる?

    # なんかでもこれを全て同時にやる切る方法がありそう

    # K個の o に対し、既に９個区切りで| がついている
    # ooooooooo | ooooooooo
    # この残りの o の隙間の、好きなところに | を打つことができる
    # それがそのまま、数になる 99 -> 189 や 981
    # この過程で、別過程なのに同じ数が生まれることはない

    # ということで、2**n 系の数になる
    # nは, 1つの9に対して 8つの隙間が生まれるので、8*(K//9)
    # -> 2**(8*(K//9)) をすればいい
    # return pow(2, 8 * (K // 9), 10 ** 9 + 7)
    return my_pow(8 * (K // 9))


def test_my_pow():
    BIG = 10 ** 9 + 7
    for k in [10, 555, 193939, 1000, 10000]:
        assert pow(2, k, BIG) == my_pow(k)


def my_pow(n):
    BIG = 10 ** 9 + 7
    product = 1
    for i in range(n):
        product *= 2
        product %= BIG
    return product


def make_nums(current, left):
    # make_nums([current], left) 的な？
    # 最後の１桁より小さい数しか選べないようにすることで、被りなく出せる?
    pass


def test_main_for_fun():
    a = main(9)
    print(a)
    b = 234 // 9
    c = b * 8
    print(c)


def test_make_nums():
    assert make_nums([1], 1) == [[1, 1]]
    assert make_nums([1], 2) == [[1, 1, 1]]
    assert make_nums([2], 1) == [[2, 1]]
