def test_main():
    inputs = [
        """7 3
atcoder
""",
        """14 5
kittyonyourlap
""",
    ]
    answers = ["acd", "inlap"]

    for text, answer in zip(inputs, answers):
        N, K = map(int, text.splitlines()[0].split())
        S = text.splitlines()[1]
        assert _main(N, K, S) == answer
        assert main(N, K, S) == answer
        assert ac(N, K, S) == answer


def ac(N, K, S):
    # c[i][j] i文字目の右にある文字jのなかで最も左側にあるもののインデックス(何文字目か)
    nex = [[-1] * 26 for _ in range(N + 1)]
    for i in range(26):
        nex[N][i] = N

    # 前計算
    for i in range(N - 1, -1, -1):
        for j in range(26):
            # 文字jに一致する場合
            if ord(S[i]) - ord("a") == j:
                nex[i][j] = i
            else:
                nex[i][j] = nex[i + 1][j]

    # 1文字ずつ貪欲に決める
    answer = ""
    current_pos = 0
    for i in range(1, K + 1):
        for j in range(26):
            # 最初の文字jを見つける
            next_pos = nex[current_pos][j]
            max_possible_length = N - next_pos - 1 + i
            if max_possible_length >= K:
                answer += chr(ord("a") + j)
                current_pos = next_pos + 1
                break
    return answer


def test_chr():
    b = ord("a") + 1
    assert chr(b) == "b"


def test_strings():
    assert "" < "a"
    assert not "" > "a"
    assert "a" > "A"
    assert "a" > "!"
    assert "a" < "}"


def main(N, K, S):
    # "" は順位が高いので、""で初期化してOK current < best にならないため
    # 端点を気にしないように、1つ多くしておく
    dp = [["|"] * (N + 1) for _ in range(K + 1)]
    S += " "  # 最後を気にしないように
    dp[0][0] = "}"  # 全てより弱い文字にしておく
    for i in range(K):
        for j in range(N):
            if dp[i][j] == "|":
                continue
            # 現在のものより優れている場合
            if S[j] < dp[i][j]:
                # 現在を更新（末尾に追加）
                dp[i][j] = S[j]
                # 右下に「与える」
                dp[i + 1][j + 1] = "}"
            if dp[i][j + 1] != "}":
                dp[i][j + 1] = min(dp[i][j], dp[i][j + 1])
    res = [dp[K - i][N - i] for i in range(1, K + 1)][::-1]
    return "".join(res)


def _main(N, K, S):
    print(N, K, S)
    # "" は順位が高いので、""で初期化してOK current < best にならないため
    # 端点を気にしないように、1つ多くしておく
    dp = [["|"] * (N + 1) for _ in range(K + 1)]
    S += " "  # 最後を気にしないように
    dp[0][0] = "}"  # 全てより弱い文字にしておく
    for i in range(K):
        for j in range(N):
            if dp[i][j] == "|":
                continue
            # 現在のものより優れている場合
            if S[j] < dp[i][j][-1]:
                # 現在を更新（末尾に追加）
                dp[i][j] = dp[i][j][:-1] + S[j]
                # 右下に「与える」
                dp[i + 1][j + 1] = dp[i][j] + "}"
            dp[i][j + 1] = min(dp[i][j], dp[i][j + 1])
    return dp[K - 1][N - 1]
