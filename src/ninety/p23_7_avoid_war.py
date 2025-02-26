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


problem = problems[0]
H, W, grid = parse_qa(problem)
logger.info(f"{H=}, {W=}, {grid=}, {problem.answer=}")
MOD = 10**9 + 7

# precompute valid states
# each state is a bitmask of W+1 bits
# a state if valid if it has at most 1 pair of adjacent 1s
# we group state by (last pari index+1); group 0 means no pair
vs = []
sg = [[] for _ in range(W + 1)]  # state groups by (last pair pos + 1)

for mask in range(1 << W + 1):
    cnt = 0
    lp = -1  # last pair position
    for j in range(W):
        if ((mask >> j) & 1) and (mask >> (j + 1) & 1):
            cnt += 1
            lp = j
            if cnt > 1:
                break
    if cnt <= 1:
        vs.append(mask)
        sg[lp + 1].append(len(vs) - 1)

# build fast lookup; map bitmask to it's index in vs
si = [0] * (1 << W + 1)
for idx, mask in enumerate(vs):
    si[mask] = idx


# dp transition
# dp by state index
# at each cell either put or no_put
# shift state left by 1
def no_put(s_idx, cur, nxt):
    # no put, just shift left
    new_mask = (vs[s_idx] * 2) % (1 << W + 1)
    nxt[si[new_mask]] += cur[s_idx]
    nxt[si[new_mask]] %= MOD


def put(s_idx, cur, nxt, col):
    # Calculate new_mask
    new_mask = ((vs[s_idx] * 2) + 1) % (1 << (W + 1))

    # For the leftmost column:
    if col == 0:
        # We must ensure that the two highest bits (positions W-2 and W-1)
        # of the current state are both 0.
        # Extract bits at positions (W-2) and (W-1) by
        # shifting right (W-2) and masking with 3 (binary 11).
        if ((vs[s_idx] >> (W - 2)) & 3) != 0:
            return

    # For the rightmost column:
    if col == W - 1:
        # Check the bits starting at position (W-1):
        #   Shift right (W-1) and mask with 3 to extract two bits.
        if ((vs[s_idx] >> (W - 1)) & 3) != 0:
            return
        # Also, ensure the least significant bit is 0 (no king immediately to the left).
        if (vs[s_idx] & 1) != 0:
            return

    # For middle columns (neither leftmost nor rightmost):
    if col not in (0, W - 1):
        # Check that all bits from position (W-2) upward are 0.
        if (vs[s_idx] >> (W - 2)) != 0:
            return
        # Also ensure the least significant bit is 0.
        if (vs[s_idx] & 1) != 0:
            return

    # If all conditions are satisfied, update the DP transition:
    nxt[si[new_mask]] = (nxt[si[new_mask]] + cur[s_idx]) % MOD


# main dp row major
# cur[state] holds the nubmer of way to have reached the state
cur = [0] * len(vs)
cur[si[0]] = 1  # start with empty state

for i in range(H):
    for j in range(W):
        nxt = [0] * len(vs)
        # process group 0 first
        # for s in sg[0]:
        for s in range(len(vs)):
            no_put(s, cur, nxt)
            if not grid[i][j]:
                put(s, cur, nxt, j)
        # process extra group to cover boundary cases
        # extra = j + W * (j == 0)
        # for s in sg[extra]:
        #     no_put(s, cur, nxt)
        #     if not grid[i][j]:
        #         put(s, cur, nxt, j)
        cur = nxt

print(sum(cur) % MOD)
