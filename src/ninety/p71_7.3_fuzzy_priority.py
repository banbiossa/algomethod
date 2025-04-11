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

parents = [set() for _ in range(N)]
children = [set() for _ in range(N)]

for a, b in A:
    a -= 1
    b -= 1
    parents[b].add(a)
    children[a].add(b)

# make d (degree) array
d = [len(x) for x in parents]

que = deque([i for i in range(N) if d[i] == 0])

path = []
while que:
    i = que.popleft()
    path.append(i)
    # d-1 for each child
    for j in children[i]:
        d[j] -= 1
        if d[j] == 0:
            que.append(j)

if len(path) != N:
    print(-1)
    exit(0)

# now we have a topological sort
print(" ".join(str(x + 1) for x in path))
