"""
N個の仕事
i: D_i が仕事の終わりの締め切り
連続するC_i日で完了する
S_i円の報酬
1日に仕事は1つ


 方針:
 - N<8 なので全探索, 2^Nを網羅する
 - N < 20 は dpぽい
 - N < 4000 は賢そう

"""


def main(N, D, C, S):
    # this is AC for subtask2
    # using dp
    # dp[i][j] = i個の仕事をj日目までに終わらせたときの最大報酬
    max_d = max(D) + 1
    assert max_d <= 5001

    # sort by deadline
    jobs = [(d, c, s) for d, c, s in zip(D, C, S)]
    jobs.sort(key=lambda x: x[0])

    dp = [[-1] * max_d for _ in range(N + 1)]
    dp[0][0] = 0
    # dp = [[0] * max_d for _ in range(N + 1)]

    for i in range(N):
        for j in range(max_d):
            if dp[i][j] == -1:
                continue
            # 仕事をやらない場合
            dp[i + 1][j] = max(dp[i + 1][j], dp[i][j])
            d, c, s = jobs[i]

            # 仕事をやる場合
            if j + c <= d:
                dp[i + 1][j + c] = max(dp[i + 1][j + c], dp[i][j] + s)

    return max(dp[N])


def main_(N, D, C, S):
    # this was AC for subtask 1
    max_revenue = 0

    for i in range(2**N):
        jobs = []
        for j in range(N):
            if i >> j & 1:
                jobs.append(j)

        # 締め切りが早い順にやらないないとダメだった
        # 始めなければダメな日、が早い順に取っていって、矛盾しなければOK
        # (が解だった気がする、自信はない）
        last_start_date = []
        for j in jobs:
            last_start_date.append((j, D[j]))
        last_start_date.sort(key=lambda x: x[1])

        total = 0
        day = 0
        is_ok = True
        for j, d in last_start_date:
            day += C[j]
            total += S[j]
            if day > d:
                is_ok = False
                break

        if not is_ok:
            continue

        max_revenue = max(max_revenue, total)

    return max_revenue


def test_main():
    inputs = [
        """1
12 3 69853
""",
        """3
7 3 200000
3 2 100000
5 3 150000
""",
        """8
376 640 602876667
4015 1868 533609371
3330 152 408704870
1874 798 30417810
2 1450 40706045
3344 1840 801881841
2853 1229 5235900
458 1277 997429858
""",
        """20
376 640 602876667
4015 868 533609371
3330 152 408704870
1874 798 30417810
2 450 40706045
3344 840 801881841
2853 229 5235900
458 277 997429858
1689 948 981897272
4774 393 997361572
4237 750 294800444
4663 293 277667068
2249 808 444906878
3341 137 845317003
3625 765 739689211
911 510 326127348
1343 193 235655766
842 323 406413067
1425 303 68833418
212 808 745744264
""",
        """30
376 140 602876667
4015 368 533609371
3330 152 408704870
1874 298 30417810
2 450 40706045
3344 340 801881841
2853 229 5235900
458 277 997429858
1689 448 981897272
4774 393 997361572
4237 250 294800444
4663 293 277667068
2249 308 444906878
3341 137 845317003
3625 265 739689211
911 10 326127348
1343 193 235655766
842 323 406413067
1425 303 68833418
212 308 745744264
3563 376 196296968
4186 323 275217640
332 361 337078801
4466 245 694789156
3763 250 432518459
2937 124 581390864
2255 227 642944345
2851 480 688009163
1957 295 5532462
3277 445 15791361
""",
    ]
    answers = [69853, 350000, 1744196082, 6583558066, 11420667389]

    for question, expected in zip(inputs, answers):
        N = int(question.splitlines()[0])
        D = []
        C = []
        S = []
        for i in range(N):
            d, c, s = map(int, question.splitlines()[i + 1].split())
            D.append(d)
            C.append(c)
            S.append(s)

        MAX_N = 20000
        if N > MAX_N:
            raise RuntimeError(f"too large {N=}, max is {MAX_N}")
        actual = main(N, D, C, S)
        assert actual == expected


if __name__ == "__main__":
    N = int(input())
    D = []
    C = []
    S = []
    for i in range(N):
        d, c, s = map(int, input().split())
        D.append(d)
        C.append(c)
        S.append(s)
    print(main(N, D, C, S))
