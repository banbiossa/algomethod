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


dp = {}
dp[0] = 1

for i in range(H):
    for j in range(W):
        pp = {}
        dp, pp = pp, dp
        for k, v in pp.items():
            bin_k = [(k >> b) & 1 for b in range(max(3, W + 1))]
            # no king
            nkey = k // 2
            dp[nkey] = dp.get(nkey, 0) + v
            dp[nkey] %= MOD

            # put a king
            if grid[i][j]:
                continue

            # left up
            if bin_k[0] and i > 0 and j > 0:
                continue
            # up
            if bin_k[1] and i > 0:
                continue
            # right up
            if bin_k[2] and i > 0 and j < W - 1:
                continue
            # left
            if bin_k[W] and j > 0:
                continue
            # put a king
            nkey = k // 2 + (1 << W)
            dp[nkey] = dp.get(nkey, 0) + v
            dp[nkey] %= MOD

ans = sum(dp.values()) % MOD
print(ans)
