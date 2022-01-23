def test_main():
    inputs = [
        """3 34
3 14
15 9
26 5
""",
        """5 77
1 16
3 91
43 9
4 26
23 11
""",
        """5 59
8 13
55 5
58 8
23 14
4 61
""",
    ]
    answers = ["BAB", "BABBA", "Impossible"]

    for text, answer in zip(inputs, answers):
        N, S = map(int, text.splitlines()[0].split())
        diff = []
        bags = []
        mins = []
        which_min = []
        for i in range(N):
            a, b = map(int, text.splitlines()[i + 1].split())
            bags.append((a, b))
            diff.append(abs(a - b))
            mins.append(min(a, b))
            which_min.append(0 if a < b else 1)
        # assert main(N, S, diff, mins, which_min) == answer
        # assert complete_search(N, S, bags) == answer
        assert dp_restore(N, S, bags) == answer


def dp_restore(N, S, bags):
    dp = [[0] * (S + 1) for _ in range(N + 1)]
    dp[0][0] = 1
    for i in range(N):
        for j in range(S + 1):
            if not dp[i][j]:
                continue
            for b in bags[i]:
                if j + b <= S:
                    dp[i + 1][j + b] = 1
    if not dp[-1][-1]:
        return "Impossible"
    # restore
    ans = []
    j = S
    for i in range(N, 0, -1):
        bag = bags[i - 1]
        if j - bag[0] >= 0 and dp[i - 1][j - bag[0]]:
            ans.append("A")
            j -= bag[0]
            continue
        if j - bag[1] >= 0 and dp[i - 1][j - bag[1]]:
            ans.append("B")
            j -= bag[1]
            continue
    return "".join(ans)[::-1]


def main(N, S, diff, mins, which_min):
    target = S - sum(mins)
    print(N, S, diff, mins, which_min)
    # 全探索してみよう
    use_bigger = set(make(target, diff))
    zero = to_zero_one(N, use_bigger, which_min)
    ab = to_ab(zero)
    return ab


def to_ab(A):
    return "".join(map(str, A)).replace("0", "A").replace("1", "B")


def test_to_ab():
    assert to_ab([0, 1, 0]) == "ABA"


def to_zero_one(N, use_bigger, which_min):
    # 変換する
    ans = [1 - which_min[i] if i in use_bigger else which_min[i] for i in range(N)]
    return ans


def test_to_zero_one():
    actual = to_zero_one(3, [0, 1], [1, 0, 0])
    assert actual == [0, 1, 0]


def test_make():
    actual = make(17, [11, 6, 21])
    assert actual == [0, 1]


def make(target, diff):
    # diff の中身で target が作れるか
    # 一旦dpでやろうか
    N = len(diff)
    dp = [[0] * (target + 1) for _ in range(N + 1)]
    dp[0][0] = 1
    for i in range(N):
        for j in range(target + 1):
            if not dp[i][j]:
                continue
            dp[i + 1][j] = 1
            if j + diff[i] <= target:
                dp[i + 1][j + diff[i]] = 1
    if not dp[-1][-1]:
        return False

    # dpを逆から辿って、使った数字を返す
    ans = []
    j = target
    for i in range(N, 0, -1):
        # 使ってない
        if dp[i][j] == dp[i - 1][j]:
            continue
        ans.append(i - 1)
        j -= diff[i - 1]
    assert sum(diff[i] for i in ans) == target
    return sorted(ans)


def complete_search(N, S, bags):
    for num in range(2 ** N):
        index = bin(num)[2:].zfill(N)
        total = sum([bags[i][int(j)] for i, j in enumerate(index)])
        if total == S:
            return index.replace("0", "A").replace("1", "B")
    return "Impossible"
