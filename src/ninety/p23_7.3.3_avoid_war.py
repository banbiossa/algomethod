import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


@dataclass
class QA:
    question: str
    answer: int


problems = [
    QA(
        question="""1 3
...
""",
        answer=5,
    ),
    QA(
        question="""3 3
.#.
#..
.##
""",
        answer=13,
    ),
    QA(
        question="""8 9
######.##
####..##.
..#...#..
###...###
#....##.#
.##......
#.####..#
#.#######
""",
        answer=273768,
    ),
]


def parse_qa(qa: QA) -> tuple:
    H, W = map(int, qa.question.split("\n")[0].split())
    # the second row is a map of the grid
    # we map . as 0 and # as 1
    # the grid should be a 2D list of 0,1
    grid = []
    for i in range(1, H + 1):
        row = qa.question.split("\n")[i]
        grid.append([1 if x == "#" else 0 for x in row])
    return H, W, grid


problem = problems[2]
H, W, grid = parse_qa(problem)
logger.info(f"{H=}, {W=}, {grid=}, {problem.answer=}")
MOD = 10**9 + 7

# using a simple dict seems to solve all the problems,
# because there are only 24*24 states

# we index with column (so max 24)
cnt = [0] * 25  # number of valid states for each column index
used = [[False] * 25 for _ in range(25)]  # 2d grid to use for dfs
state = [[] for _ in range(25)]  # state[i] holds valid states for column i
map_state = [{} for _ in range(25)]  # map_state[i] maps state to (idx, flag)
nex0 = [{} for _ in range(25)]  # for each column i, next state index when no king
nex1 = [{} for _ in range(25)]  # for each column, next state when placing


def hantei(sx, sy):
    dx = [1, 1, 1, 0, -1, -1, -1, 0]
    dy = [-1, 0, 1, 1, 1, 0, -1, -1]
    for i in range(8):
        tx = sx + dx[i]
        ty = sy + dy[i]
        if tx < 0 or ty < 0 or ty >= W:
            continue
        if used[tx][ty]:
            return False
    return True


def dfs(pos, dep, s):
    """dfs that builds a binary string of length W+1

    Args:
        pos: current index in a virtual 1d array (sx, sy)
        dep: depth (num characters in the binary string)
        s: current state string (e.g. "010...")
    """
    sx = pos // W
    sy = pos % W
    if dep == W + 1:
        # when the state is complete, record it for column 'sy'
        flag = hantei(sx, sy)
        idx = cnt[sy]
        state[sy].append(s)
        map_state[sy][s] = (idx, flag)
        cnt[sy] += 1
        return
    # 1. no king
    dfs(pos + 1, dep + 1, s + "0")
    # 2. king
    if hantei(sx, sy):
        used[sx][sy] = True
        dfs(pos + 1, dep + 1, s + "1")
        used[sx][sy] = False


# precompute valid states for each column position
for i in range(W):
    dfs(i, 0, "")

# precompute state transitions
# for each column sy and each state s
# we compute the next state after shifting and appending 0
for i in range(W):
    # initialize nex0 and nex1 for column i
    nex0[i] = [None] * cnt[i]
    nex1[i] = [None] * cnt[i]

    for j in range(cnt[i]):
        t = state[i][j]
        # create shifted state
        t0 = t[1:] + "0"
        t1 = t[1:] + "1"
        # look up the next state
        nxt_idx0, _ = map_state[(i + 1) % W][t0]
        nex0[i][j] = nxt_idx0
        # for the state with a king placed, check flag
        _, flag = map_state[i][t]
        if flag:
            nxt_idx1, _ = map_state[(i + 1) % W][t1]
            nex1[i][j] = nxt_idx1
        else:
            nex1[i][j] = -1  # invaild transition

# setup the 3d dp table
# dp[r][c][idx] = number of ways to fill the grid up to r,c
dp = [[[0] * cnt[j] for j in range(W)] for _ in range(H + 1)]
dp[0][0][0] = 1

for i in range(H):
    for j in range(W):
        n1, n2 = i, j + 1
        if n2 == W:
            n1 += 1
            n2 = 0

        for k in range(cnt[j]):
            if dp[i][j][k] == 0:
                continue
            # no king
            nxt = nex0[j][k]
            dp[n1][n2][nxt] += dp[i][j][k]
            dp[n1][n2][nxt] %= MOD
            # put king
            if nex1[j][k] != -1 and grid[i][j] == 0:
                nxt = nex1[j][k]
                dp[n1][n2][nxt] += dp[i][j][k]
                dp[n1][n2][nxt] %= MOD

ans = sum(dp[H][0]) % MOD
print(ans)
