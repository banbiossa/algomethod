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


# for the H, W <= 17 case, we use dp but for W+1
# the previous states because like
# _ x x x
# _ x o
# in this case, only the x's matter (W+1)
# in another case
# . . . _
# x x _ _
# o
# only the x's matter, so which of the W+1 bits matter
# depend on the column

dp = [[[0] * (1 << (1 + W)) for _ in range(W)] for _ in range(H + 1)]
# not sure of 0,0,0 == 1 is valid, come back later
dp[0][0][0] = 1

logger.debug(f"dim {len(dp), len(dp[0])}")

for i in range(H):
    for j in range(W):
        for k in range(1 << (W + 1)):
            # skip if 0 for convience in logging
            if dp[i][j][k] == 0:
                continue

            dp[i][j][k] %= MOD
            logger.debug(f"{i=}, {j=}, {k=}")
            logger.debug(f"{dp[i][j]=}")

            # calculate next row
            if j == W - 1:
                next_i = i + 1
                next_j = 0
            else:
                next_i = i
                next_j = j + 1

            # no king
            logger.debug(f"{next_i=}, {next_j=}, {k//2=}")
            dp[next_i][next_j][k // 2] += dp[i][j][k]
            dp[next_i][next_j][k // 2] %= MOD

            # put a king
            if grid[i][j]:
                logger.debug(f"skip grid {i=}, {j=}")
                continue

            # check if we can put a king
            # represent k as a binary string
            # max 3 because we always check bin_k[2]
            bin_k = [(k >> b) & 1 for b in range(max(3, W + 1))]

            logger.debug(f"{bin_k=}")
            # left up is hit (bin[0] is hit)
            # x _ _
            # _ o
            if bin_k[0] and i >= 1 and j >= 1:
                logger.debug(f"skip left up {i=}, {j=}")
                continue
            # bin[1] is hit = up is hit
            if bin_k[1] and i >= 1:
                logger.debug(f"skip up {i=}, {j=}")
                continue
            # bin[2] is hit = right up is hit
            if bin_k[2] and i >= 1 and j < W - 1:
                logger.debug(f"skip right up {i=}, {j=}")
                continue
            # bin[W] is hit = left is hit
            if bin_k[W] and j >= 1:
                logger.debug(f"skip left {i=}, {j=}")
                continue

            logger.debug(f"put in {next_i=}, {next_j=}, {k//2 + (1 << W)=}")
            dp[next_i][next_j][k // 2 + (1 << W)] += dp[i][j][k]
            dp[next_i][next_j][k // 2 + (1 << W)] %= MOD

            logger.debug(f"{dp[next_i][next_j]=}")


# the final result is the sum of the last row
logger.info(f"{dp[H][0]=}")

# take modulo
total = 0
for i in dp[H][0]:
    total += i
    total %= MOD
print(total)
