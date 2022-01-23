def test_main():
    inputs = [
        """3 3
...
.#.
...
""",
        """1 6
......
""",
        """4 4
....
#...
....
...#
""",
    ]

    answers = [8, -1, 12]

    for text, answer in zip(inputs, answers):
        H, W = map(int, text.splitlines()[0].split())
        S = []
        for i in range(H):
            S.append(text.splitlines()[i + 1])

        assert main(H, W, S) == answer


def main(H, W, S):
    ans = -1
    for i, j in itertools.product(range(H), range(W)):
        loop = Loop(H, W, S)
        ans = max(ans, loop.dfs(i, j, i, j))
    if ans <= 2:
        return -1
    return ans


class Loop:
    def __init__(self, H, W, S):
        self.H = H
        self.W = W
        self.S = S
        self.used = [[False] * W for _ in range(H)]

    def dfs(self, sx, sy, px, py):
        if sx == px and sy == py and self.used[px][py]:
            return 0
        self.used[px][py] = True
        ret = -10000
        for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            nx = px + dx
            ny = py + dy
            if not ((0 <= nx < self.H) and (0 <= ny < self.H)):
                continue
            if self.S[nx][ny] == "#":
                continue
            if (sx != nx or sy != ny) and self.used[nx][ny]:
                continue
            v = self.dfs(sx, sy, nx, ny)
            ret = max(ret, v + 1)
        self.used[px][py] = False
        return ret


import itertools


def _main(H, W, S):
    # 見た目的には2*2のブロックがあると、行って帰ってこれる
    # H, W <= 16なので、結構無理のあるアルゴリズムで良さそう
    # ブロックのサイズは2*2 -> 3*3 -> ... -> n*n
    # と大きくしていく必要がありそう
    print(H, W, S)

    # in_loopというdpを持つ
    # loop が2つ以上ないことを前提とする。。。
    # 最初のループに入っていない点からスタートして全探索、もあり得そう

    # 全探索と再帰関数
    visited = [[False] * W for _ in range(H)]
    longest = 0
    best_path = None
    for (sx, sy) in itertools.product(range(H), range(W)):
        length, path = find_loop(sx, sy, H, W, S, visited.copy(), 1, [])
        if length > longest:
            length = longest
            best_path = path
    return longest


def back_track(sx, sy, H, W, S, visited, length, path):
    # 素直にbacktrackを実装する
    # out of range
    if not ((0 <= sx < H) and (0 <= sy < W)):
        return -1, path

    # 壁
    if S[sx][sy] == "#":
        return -1, path

    # found loop
    if visited[sx][sy]:
        return length, path
    visited[sx][sy] = True
    path.append((sx, sy))

    best_ans = 0
    best_path = None
    for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
        x = sx + dx
        y = sx + dy
        ans, current_path = find_loop(x, y, H, W, S, visited.copy(), length + 1, path)
        if ans > best_ans:
            best_ans = ans
            best_path = current_path
    return best_ans, best_path


def find_loop(sx, sy, H, W, S, visited, length, path):
    # out of range
    if not ((0 <= sx < H) and (0 <= sy < W)):
        return -1, path

    # 壁
    if S[sx][sy] == "#":
        return -1, path

    # found loop
    if visited[sx][sy]:
        return length, path
    visited[sx][sy] = True
    path.append((sx, sy))

    best_ans = 0
    best_path = None
    for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
        x = sx + dx

        y = sx + dy
        ans, current_path = find_loop(x, y, H, W, S, visited.copy(), length + 1, path)
        if ans > best_ans:
            best_ans = ans
            best_path = current_path

    return best_ans, best_path
