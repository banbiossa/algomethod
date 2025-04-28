"""how the planes move
4 3 2
5 d 1
6 7 8

the data input
N T
ax1 ay1
...
axN ayN
bx1 by1
...
bxN byN
"""

import sys

# set the maximum recursion depth to a large number
sys.setrecursionlimit(10**6)

problems = [
    (
        """3 2
3 3
5 5
9 2
11 2
5 5
3 3
""",
        """Yes
2 6 1
""",
    )
]


import os


def get_env():
    if os.path.exists(".env"):
        return "DEBUG"
    return "PROD"


def parse_input(input_str):
    lines = input_str.strip().split("\n")
    n, t = map(int, lines[0].split())
    ax = [0]
    ay = [0]
    for i in range(1, n + 1):
        x, y = map(int, lines[i].split())
        ax.append(x)
        ay.append(y)
    bx = [0]
    by = [0]
    for i in range(n + 1, 2 * n + 1):
        x, y = map(int, lines[i].split())
        bx.append(x)
        by.append(y)
    return n, t, ax, ay, bx, by


def parse_io():
    n, t = map(int, input().split())
    ax = [0]  # allow for 1-index
    ay = [0]
    for _ in range(n):
        x, y = map(int, input().split())
        ax.append(x)
        ay.append(y)
    bx = [0]
    by = [0]
    for _ in range(n):
        x, y = map(int, input().split())
        bx.append(x)
        by.append(y)
    return n, t, ax, ay, bx, by


ENV = get_env()


def parse(p):
    if ENV == "DEBUG":
        return parse_input(p)
    else:
        return parse_io()


problem = problems[0]

N, T, AX, AY, BX, BY = parse(problem[0])

import logging  # noqa

if ENV == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger(__name__)

logger.info(f"{N=}, {T=}, {AX=}, {AY=} {BX=} {BY=}")


# for the second case Ay=By=0, so we can ignore y
# i think by starting from the B side, we can limit the number of
# 候補.

# we make a graph of the planes
# red:  -T     +T
#         \  /
# blue:  original
# if the number of red==blue, we can find a solution


G = [[] for _ in range(2 * N + 1)]

# make map
inv_map = {}
for i in range(1, N + 1):
    inv_map[BX[i]] = i

logger.info(f"{inv_map=}")

# make graph
for i in range(1, N + 1):
    idx1 = inv_map.get(AX[i] - T, 0)
    idx2 = inv_map.get(AX[i] + T, 0)

    if idx1 != 0:
        G[i].append(idx1 + N)
        G[idx1 + N].append(i)
    if idx2 != 0:
        G[i].append(idx2 + N)
        G[idx2 + N].append(i)

used = [False] * (2 * N + 1)
cnta = 0
cntb = 0
Answer = [0] * (N + 1)


def dfs(pos: int, pre: int):
    global cnta, cntb
    used[pos] = True
    if pos <= N:
        cnta += 1
    if pos > N:
        cntb += 1
        if AX[pre] < BX[pos - N]:
            Answer[pre] = 1
        if AX[pre] > BX[pos - N]:
            Answer[pre] = 5
    for i in G[pos]:
        if not used[i]:
            dfs(i, pos)


# dfs
for i in range(1, N + 1):
    if len(G[i]) >= 2 or used[i]:
        continue
    cnta = 0
    cntb = 0
    dfs(i, -1)
    if cnta != cntb:
        print("No")
        exit(0)

# output
print("Yes")
# print answer 1:
print(" ".join(map(str, Answer[1:])))
