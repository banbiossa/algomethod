def test_main():
    inputs = [
        """3
1 2
3 6
7 4
""",
        """3
1 2
2 2
4 2
""",
        """4
0 0
0 1000000000
1000000000 0
1000000000 1000000000
""",
    ]
    answers = [
        6,
        2,
        8,
    ]
    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        machi = []
        for i in range(N):
            machi.append(tuple(map(int, text.splitlines()[i + 1].split())))
        assert main(N, machi) == answer


def gcd(A, B):
    A = abs(A)
    B = abs(B)
    if B == 0:
        return A
    return gcd(B, A % B)


def main(N, machi):
    # 全てのペアについて、diff_x, diff_y  を最大公約数で割る
    # これを set に記憶する
    # この長さを返す
    spell = set()
    for i in range(N):
        for j in range(i + 1, N):
            diff_x = machi[i][0] - machi[j][0]
            diff_y = machi[i][1] - machi[j][1]
            if diff_x == 0:
                spell.add((0, 1))
                spell.add((0, -1))
            elif diff_y == 0:
                spell.add((1, 0))
                spell.add((-1, 0))
            else:
                g = gcd(diff_x, diff_y)
                spell.add((diff_x // g, diff_y // g))
                spell.add((-diff_x // g, -diff_y // g))
    return len(spell)

iam = "a user"
print("hello")
print("yes")