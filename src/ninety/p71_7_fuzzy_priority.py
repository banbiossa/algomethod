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

# my second guess
# make a parents = [{}, ...] and just search there
parents = [set() for _ in range(N)]
for i in range(M):
    a, b = A[i]
    a -= 1
    b -= 1
    parents[b].add(a)

logger.info(f"{parents=}")


def find(visited: list):
    if len(visited) == N:
        yield visited
        return
    for i in range(N):
        if i in visited:
            continue
        # check if all parents are visited
        if not parents[i].issubset(visited):
            continue
        # we can add to path and go deeper
        yield from find(visited + [i])


# find all the paths
good = []
for path in find([]):
    good.append(path)
    if len(good) == K:
        break

if len(good) < K:
    print(-1)
    exit(0)
else:
    for i in range(K):
        print(" ".join(str(x + 1) for x in good[i]))


# my first guess
# 1. make a connected graph of the Ai and Bi
#  1.1 [0,1,2] [3,4] [5]
# 2. DFS to find all the paths
#  2.1 at each intersection, you can choose one head
#   2.1.1 eg. 0 or 3 or 5

# the diffucult case is when you have multiple heads
# so like
# 0    5
# | \ /
# 1  2
# |  |
# 3  4
# in this case, if you pop 0, [1,3] and [2,4]
# will be added as "heads"

# so we need some kind of tree structure
# to keep track of the heads


# class Node:
#     def __init__(self, value: int):
#         self.value = value
#         self.children: list[Node] = []
#         self.parents: list[Node] = []
#         self.visited = False

#     def add_child(self, child: Node):
#         self.children.append(child)
#         child.parents.append(self)

#     def __repr__(self):
#         return f"Node({self.value})->{self.children}"


# nodes = [Node(i) for i in range(N)]

# # add the edges (a graph)
# for i in range(M):
#     a, b = A[i]
#     a -= 1
#     b -= 1
#     nodes[a].add_child(nodes[b])


# logger.info(f"{nodes=}")


# from collections import deque

# que = deque([n for n in nodes if not n.parents])
# logger.info(f"initial {que=}")

# good = []
