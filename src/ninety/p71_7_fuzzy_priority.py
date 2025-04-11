from __future__ import annotations

# N M K
# A1 B1
# ...
# AM BM
# ---
# P1 ... PN


problems = [
    (
        """5 2 3
1 2
3 4
""",
        """1 2 3 4 5
1 3 2 4 5
1 3 5 2 4""",
    ),
    (
        """5 2 1
1 3
3 1
""",
        "-1",
    ),
]


def get_env():
    # returns DEBUG if can find a .env file
    # else returns PROD
    import os

    if os.path.exists(".env"):
        return "DEBUG"
    return "PROD"


import logging

ENV = get_env()
if ENV == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def parse_input(input_str):
    lines = input_str.strip().split("\n")
    n, m, k = map(int, lines[0].split())
    a = []
    for i in range(1, m + 1):
        a.append(tuple(map(int, lines[i].split())))
    return n, m, k, a


def parse_io():
    n, m, k = map(int, input().split())
    a = []
    for _ in range(m):
        a.append(tuple(map(int, input().split())))
    return n, m, k, a


def parse(p):
    if ENV == "DEBUG":
        return parse_input(p[0])
    else:
        return parse_io()


problem = problems[0]
N, M, K, A = parse(problem)

logger.info(f"{N=}, {M=}, {K=}, {A=}")

# first question is N<10**3 so a dumb solution is ok
# find k permutations where Ai comes before Bi

# we can use topological sort for the k=1 case
# naive: find a node with no parent and remove
# fast: d_i: degree of i, put in queue, d-=1 for each child

# now we make this fast with queue
from collections import deque  # noqa


# let's start with naive
# -> as intended, q2 is TLE (not WA)
parents = [set() for _ in range(N)]

for a, b in A:
    a -= 1
    b -= 1
    parents[b].add(a)

# we only find 1 path
path = []
used = [False] * N
while True:
    if len(path) == N:
        print(" ".join(str(x + 1) for x in path))
        exit(0)
        break

    choose = False
    for i in range(N):
        if len(parents[i]) != 0 or used[i]:
            continue
        path.append(i)
        used[i] = True
        choose = True

        # remove i from all parents
        for j in range(N):
            if i in parents[j]:
                parents[j].remove(i)

    # we weren't able to find a node
    if not choose:
        print(-1)
        exit(0)
        break
