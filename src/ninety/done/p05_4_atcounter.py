def test_main():
    inputs = [
        """10
attcordeer
""",
        """41
btwogablwetwoiehocghiewobadegwhoihegnldir
""",
        """140
aaaaaaaaaaaaaaaaaaaattttttttttttttttttttccccccccccccccccccccooooooooooooooooooooddddddddddddddddddddeeeeeeeeeeeeeeeeeeeerrrrrrrrrrrrrrrrrrrr
""",
    ]

    answers = [
        4,
        2,
        279999993,
    ]

    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        S = text.splitlines()[1]
        assert main(N, S) == answer


def main(N, S):
    """do dp with clean S"""
    BIG = 10 ** 9 + 7
    # N = len(S)
    target = "atcoder"
    T = len(target)
    dp = [[0] * (N + 1) for _ in range(T + 1)]

    # 0行目は1
    # dp[0] = [1] * (T + 1)
    dp[0][0] = 1

    # loop(配るように考える)
    for i, t in enumerate(target):
        for j, s in enumerate(S):
            # 一致する場合は dp[i-1][j] + dp[i][j-1]
            if t == s:
                dp[i + 1][j] += dp[i][j]
                dp[i + 1][j] %= BIG
            # 一致しない場合は dp[i][j-1]
            dp[i][j + 1] += dp[i][j]
            dp[i][j + 1] %= BIG

    # もらうdp的には最後の行も += dp[i][j]したい
    # それは行のsumを取るのと等価な気がする
    total = 0
    for a in dp[-1]:
        total += a
        total %= BIG
    return total


def do_dp(S):
    N = len(S)
    BIG = 10 ** 9 + 7
    target = "atcoder"
    T = len(target)
    dp = [[0] * (N + 1) for _ in range(T + 1)]

    # 0行目は1
    # dp[0] = [1] * (T + 1)
    dp[0][0] = 1

    # loop(配るように考える)
    for i, t in enumerate(target):
        for j, s in enumerate(S):
            # 一致する場合は dp[i-1][j] + dp[i][j-1]
            if t == s:
                dp[i + 1][j + 1] += dp[i][j]
                dp[i + 1][j + 1] %= BIG
            # 一致しない場合は dp[i][j-1]
            dp[i][j + 1] += dp[i][j]
            dp[i][j + 1] %= BIG

    return dp[-1][-1]


def test_do_dp():
    assert do_dp("atcoder") == 1
    assert do_dp("atatcoder") == 3
    assert do_dp("atattcoder") == 5


def running_count(S):
    """keep a running count"""
    res = []
    running = 0
    current = ""
    for s in S:
        if s == current:
            running += 1
        else:
            if current != "":
                res.append((current, running))
            running = 1
            current = s
    res.append((current, running))
    return res


def test_running_count():
    assert running_count("aaat") == [("a", 3), ("t", 1)]
    assert running_count("aaatdd") == [("a", 3), ("t", 1), ("d", 2)]


def strip(S):
    use = {"a", "t", "c", "o", "d", "e", "r"}
    return "".join([s for s in S if s in use])


def test_strip():
    assert strip("aaatbb") == "aaat"
    assert strip("btwogablwetwoiehocghiewobadegwhoihegnldir") == "toaetoeoceoadeoedr"
