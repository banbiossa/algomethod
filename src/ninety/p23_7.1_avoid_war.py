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
    # we map . as 1 and # as 0
    grid = [[1 if x == "." else 0 for x in y] for y in qa.question.split("\n")[1:-1]]
    return H, W, grid


problem = problems[2]
H, W, grid = parse_qa(problem)
logger.info(f"{H=}, {W=}, {grid=}, {problem.answer=}")

# first case is H, W <= 4 so we can brute force it
# for each cell, we can either put or not put a king
# check if putting is a legal move


def dfs(grid, kings, h, w) -> int:
    """will do a dfs(recursion) to check if kings can be placed.
    in the base case, a 1 will be returned on a successful placement of kings
    or legal move. 0 shouldn't be returned if we do if right.

    Args:
        grid (_type_): _description_
        kings (_type_): _description_
        h (_type_): _description_
        w (_type_): _description_

    Returns:
        int: _description_
    """
    logger.debug(f"{h=}, {w=}, {kings=}, {grid=}")
    # base case
    if h == H:
        logger.info(f"base case {kings=}, {h=}, {w=}")
        return 1

    # if we are at the end of the row, move to the next row
    if w == W - 1:
        next_h = h + 1
        next_w = 0
    else:
        next_h = h
        next_w = w + 1

    # call the case where you don't put a king
    dont_put = dfs(grid, kings, next_h, next_w)

    # in the case of put, we check if putting a king in h, w is legal
    # illegal if not a white cell
    if grid[h][w] == 0:
        logger.debug(f"illegal move at {h=}, {w=}")
        return dont_put

    # illegal if there is king within [-1, 1] on either side
    # boundary checks necessary for each point
    # left
    if w > 0 and kings[h][w - 1] == 1:
        logger.debug(f"DONT king on {h=}, {w-1=}, {kings=}")
        return dont_put
    # right
    if w < W - 1 and kings[h][w + 1] == 1:
        logger.debug(f"DONT king on {h=}, {w+1=}, {kings=}")
        return dont_put
    # down
    if h > 0 and kings[h - 1][w] == 1:
        logger.debug(f"DONT king on {h-1=}, {w=}, {kings=}")
        return dont_put
    # up
    if h < H - 1 and kings[h + 1][w] == 1:
        logger.debug(f"DONT king on {h+1=}, {w=}, {kings}")
        return dont_put

    # we have passed all checks, this is a legal move so put a king
    logger.info(f"putting king at {h=}, {w=}")
    kings[h][w] = 1
    do_put = dfs(grid, kings, next_h, next_w)
    logger.info(f"returning {h=}, {w=}, {do_put=}, {dont_put=}")

    return dont_put + do_put


# ans = dfs(grid, [[0] * W for _ in range(H)], 0, 0)
# print(ans)

from collections import deque
from copy import deepcopy

MOD = 10**9 + 7

initial_kings = [[0] * W for _ in range(H)]
que = deque([(initial_kings, 0, 0)])

total = 0

while que:
    logger.debug(f"{que=}")
    kings, h, w = que.popleft()
    logger.debug(f"{h=}, {w=}, {kings=}")
    if h == H:
        total += 1
        total %= MOD
        logger.info(f"GOOD ANSWER: {kings=}, total {total=}")
        continue

    # if we are at the end of the row, move to the next row
    if w == W - 1:
        next_h = h + 1
        next_w = 0
    else:
        next_h = h
        next_w = w + 1

    # call the case where you don't put a king
    que.append((deepcopy(kings), next_h, next_w))

    # in the case of put, we check if putting a king in h, w is legal
    # illegal if not a white cell
    if grid[h][w] == 0:
        logger.debug(f"illegal move at {h=}, {w=}")
        continue

    # illegal if there is king within [-1, 1] on either side
    # boundary checks necessary for each point
    # left
    if w > 0 and kings[h][w - 1] == 1:
        logger.debug(f"DONT king on {h=}, {w-1=}, {kings=}")
        continue
    # right
    if w < W - 1 and kings[h][w + 1] == 1:
        logger.debug(f"DONT king on {h=}, {w+1=}, {kings=}")
        continue
    # down
    if h > 0 and kings[h - 1][w] == 1:
        logger.debug(f"DONT king on {h-1=}, {w=}, {kings=}")
        continue
    # up
    if h < H - 1 and kings[h + 1][w] == 1:
        logger.debug(f"DONT king on {h+1=}, {w=}, {kings}")
        continue
    # left-up
    if h > 0 and w > 0 and kings[h - 1][w - 1] == 1:
        logger.debug(f"DONT king on {h-1=}, {w-1=}, {kings}")
        continue
    # right up
    if h > 0 and w < W - 1 and kings[h - 1][w + 1] == 1:
        logger.debug(f"DONT king on {h-1=}, {w+1=}, {kings}")
        continue
    # left down
    if h < H - 1 and w > 0 and kings[h + 1][w - 1] == 1:
        logger.debug(f"DONT king on {h+1=}, {w-1=}, {kings}")
        continue
    # right down
    if h < H - 1 and w < W - 1 and kings[h + 1][w + 1] == 1:
        logger.debug(f"DONT king on {h+1=}, {w+1=}, {kings}")
        continue

    # we have passed all checks, this is a legal move so put a king
    logger.info(f"putting king at {h=}, {w=}")
    kings[h][w] = 1
    que.append((deepcopy(kings), next_h, next_w))

print(total)
