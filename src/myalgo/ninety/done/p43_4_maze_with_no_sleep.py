from collections import deque


def test_main():
    inputs = [
        """3 3
1 1
3 3
..#
#.#
#..
""",
        """3 3
2 1
2 3
#.#
...
#.#
""",
        """4 6
2 1
1 5
...#..
.#.##.
.#....
...##.
""",
    ]
    answers = [2, 0, 5]
    for text, answer in zip(inputs, answers):
        H, W = map(int, text.splitlines()[0].split())
        rs, cs = map(lambda x: int(x) - 1, text.splitlines()[1].split())
        rt, ct = map(lambda x: int(x) - 1, text.splitlines()[2].split())
        S = [] * H
        for i in range(H):
            S.append(text.splitlines()[i + 3])
        assert main(H, W, rs, rt, cs, ct, S) == answer
        assert ac(H, W, rs, rt, cs, ct, S) == answer
        assert fast(H, W, rs, rt, cs, ct, S) == answer


def faster(H, W, rs, rt, cs, ct, S):
    # 向きに応じて4つのdpを持っておく
    # 0: up 1: right 2: down 3: left
    dp = [[[1 << 32] * 4 for _ in range(W)] for _ in range(H)]

    Q = deque([(rs, cs, 0), (rs, cs, 1), (rs, cs, 2), (rs, cs, 3)])
    # スタート地点は距離0
    for i in range(4):
        dp[rs][cs][i] = 0
    # 通れないところは -1
    for i in range(H):
        for j in range(W):
            if S[i][j] == "#":
                for k in range(4):
                    dp[i][j][k] = -1

    while Q:
        r, c, direction = Q.popleft()
        current = dp[r][c][direction]
        for i, (dr, dc) in enumerate([[1, 0], [0, 1], [-1, 0], [0, -1]]):
            # 範囲外
            rn = r + dr
            cn = c + dc
            if not ((0 <= rn < H) and (0 <= cn < W)):
                continue
            # 壁
            if dp[rn][cn][i] == -1:
                continue
            # same direction
            if i == direction:
                # 最小値ならappend
                if dp[rn][cn][i] > current:
                    dp[rn][cn][i] = current
                    Q.appendleft((rn, cn, i))
            # different direction
            else:
                # 最小値ならappend
                if dp[rn][cn][i] > current + 1:
                    dp[rn][cn][i] = current + 1
                    Q.append((rn, cn, i))

        if (r == rt) and (c == ct):
            break

    return min(dp[rt][ct])


def fast(H, W, rs, rt, cs, ct, S):
    # 向きに応じて4つのdpを持っておく
    # 0: up 1: right 2: down 3: left
    dp = [[[1 << 32] * 4 for _ in range(W)] for _ in range(H)]

    Q = deque([(rs, cs, 0), (rs, cs, 1), (rs, cs, 2), (rs, cs, 3)])
    # スタート地点は距離0
    for i in range(4):
        dp[rs][cs][i] = 0

    while Q:
        r, c, direction = Q.popleft()
        current = dp[r][c][direction]
        for i, (dr, dc) in enumerate([[1, 0], [0, 1], [-1, 0], [0, -1]]):
            # 範囲外
            rn = r + dr
            cn = c + dc
            if not ((0 <= rn < H) and (0 <= cn < W)):
                continue
            # 壁
            if S[rn][cn] == "#":
                continue
            # same direction
            if i == direction:
                # 最小値ならappend
                if dp[rn][cn][i] > current:
                    dp[rn][cn][i] = current
                    Q.appendleft((rn, cn, i))
            # different direction
            else:
                # 最小値ならappend
                if dp[rn][cn][i] > current + 1:
                    dp[rn][cn][i] = current + 1
                    Q.append((rn, cn, i))

        if (r == rt) and (c == ct):
            break

    return min(dp[rt][ct])


def ac(H, W, rs, rt, cs, ct, S):
    # 向きに応じて4つのdpを持っておく
    # 0: up 1: right 2: down 3: left
    dp = [[[1 << 32] * 4 for _ in range(W)] for _ in range(H)]

    Q = deque([(rs, cs, 0, 0), (rs, cs, 1, 0), (rs, cs, 2, 0), (rs, cs, 3, 0)])
    while Q:
        r, c, direction, current = Q.popleft()

        # 範囲外
        if not ((0 <= r < H) and (0 <= c < W)):
            continue

        # 壁
        if S[r][c] == "#":
            continue

        # 現在の向きで最少であれば、他の向きを追加しても良い
        # not minimum
        if current >= dp[r][c][direction]:
            continue

        dp[r][c][direction] = current
        if r == rt and c == ct:
            break
        for i, (dr, dc) in enumerate([[1, 0], [0, 1], [-1, 0], [0, -1]]):
            # same direction
            if i == direction:
                Q.appendleft((r + dr, c + dc, i, current))
            # different direction
            else:
                Q.append((r, c, i, current + 1))

    return min(dp[rt][ct])


def main(H, W, rs, rt, cs, ct, S):
    # シンプルに幅優先探索でよさそう
    # ただし現状までの最小値をdpとしてもち、現在の移動方向も記憶する

    dp = [[1 << 32] * W for _ in range(H)]
    Q = deque([(rs, cs, 0, None)])
    while Q:
        r, c, current, direction = Q.popleft()

        # 範囲外
        if not ((0 <= r < H) and (0 <= c < W)):
            continue

        # 壁
        if S[r][c] == "#":
            continue

        # not minimum
        if current >= dp[r][c]:
            continue

        dp[r][c] = current
        for dr, dc in ([1, 0], [-1, 0], [0, 1], [0, -1]):
            # count change of direction
            if direction is None or (dr, dc) == direction:
                num = current
            else:
                num = current + 1
            Q.append((r + dr, c + dc, num, (dr, dc)))

    return dp[rt][ct]
