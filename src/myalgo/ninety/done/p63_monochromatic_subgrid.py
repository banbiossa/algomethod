def test_main():
    inputs = [
        """4 6
1 1 1 1 1 2
1 2 2 2 2 2
1 2 2 3 2 3
1 2 3 2 2 3
""",
        """3 3
1 2 3
4 5 6
7 8 9
""",
        """5 3
7 7 7
7 7 7
7 7 7
7 7 7
7 7 7
""",
    ]
    answers = [
        6,
        1,
        15,
    ]
    for text, answer in zip(inputs, answers):
        H, W = map(int, text.splitlines()[0].split())
        P = []
        for i in range(H):
            P.append(list(map(int, text.splitlines()[i + 1].split())))

        assert main(H, W, P) == answer


from collections import defaultdict


def main(H, W, P):
    # Hをbit全探索
    total = 0
    for i in range(1, 2**H):
        bits = bin(i)[2:].zfill(H)
        userows = [i for i, b in enumerate(bits) if b == "1"]

        # total = maximum_same(userows, P)
        ret = 0
        d = defaultdict(int)
        for j in range(W):
            nums = list(set(P[row][j] for row in userows))
            if len(nums) == 1:
                d[nums[0]] += 1
                ret = max(ret, d[nums[0]])
        total = max(total, len(userows) * ret)

    return total
