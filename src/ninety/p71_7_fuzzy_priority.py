from __future__ import annotations

import sys

sys.setrecursionlimit(10**6)

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

# for the first case, we do a simple DFS
# for the next case, we do an optimized DFS

G = [[] for _ in range(N)]
di = [0] * N

for a, b in A:
    a -= 1
    b -= 1
    di[b] += 1
    G[a].append(b)

# we copy other people's code
from collections import deque  # noqa
import copy  # noqa

que = deque([i for i, x in enumerate(di) if x == 0])

# path, di, next
all_que = deque([([], di, que)])

res = []
while all_que:
    if len(res) == K:
        break
    path, d, q = all_que.popleft()

    # end if their's nothing to do
    if not q:
        if len(path) == N:
            res.append(path)
            continue
        else:
            break

    # if there's only 1 in que use that
    if len(q) == 1 or len(all_que) >= K - len(res) - 1:
        v = q.popleft()
        path.append(v)
        for u in G[v]:
            d[u] -= 1
            if d[u] == 0:
                q.append(u)
        all_que.append((path, d, q))
        continue

    # use top K if there's more than 1
    ct = min(len(q), K - len(all_que) - len(res))
    if ct <= 0:
        continue
    for i in range(ct):
        d1 = d[:]
        path1 = path[:]
        q1 = copy.deepcopy(q)
        v = q[i]
        path1.append(v)
        del q1[i]
        for u in G[v]:
            d1[u] -= 1
            if d1[u] == 0:
                q1.append(u)
        all_que.append((path1, d1, q1))

if len(res) < K:
    print(-1)
else:
    for r in res:
        print(" ".join(str(x + 1) for x in r))
