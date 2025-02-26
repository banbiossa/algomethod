import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.WARNING)
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
    # make grid a list of binary numbers
    grid = []
    for i in range(1, H + 1):
        row = qa.question.split("\n")[i]
        grid.append(int(row.replace(".", "0").replace("#", "1"), 2))
    return H, W, grid


problem = problems[2]
H, W, grid = parse_qa(problem)
logger.info(f"{H=}, {W=}, {grid=}, {problem.answer=}")


# for the H, W <= 9 case, we can use bit dp
# dp[num_row][state of the previous row]  # num valid states
# this is because the previous row determines if the current
# row is vaild or not

dp = [[0] * (1 << W) for _ in range(H + 1)]
# not sure of 0,0 == 1 is valid, come back later
dp[0][0] = 1

for i in range(H):
    for j in range(1 << W):
        # for all cases of what you can put on row i
        for k in range(1 << W):
            # check if valid
            # this is check between j and k
            if k & j or k & (j << 1) or k & (j >> 1):
                logger.debug(f"skip {j=}, {k=}")
                continue
            # check between k and k
            if k & (k << 1) or k & (k >> 1):
                logger.debug(f"skip {k=}")
                continue
            # also grid and k
            if k & grid[i]:
                logger.debug(f"skip {k=}, {grid[i]=}")
                continue
            # if valid, add
            logger.info(f"add {i=}, {j=}, {k=}, {dp[i][j]=}")
            dp[i + 1][k] += dp[i][j]

# the final result is the sum of the last row
logger.info(f"{dp=}")

# take modulo
MOD = 10**9 + 7
total = 0
for i in range(1 << W):
    total += dp[H][i]
    total %= MOD
print(total)
