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
    a = []
    for i in range(1, n + 1):
        a.append(tuple(map(int, lines[i].split())))
    b = []
    for i in range(n + 1, 2 * n + 1):
        b.append(tuple(map(int, lines[i].split())))
    return n, t, a, b


def parse_io():
    n, t = map(int, input().split())
    a = []
    for _ in range(n):
        a.append(tuple(map(int, input().split())))
    b = []
    for _ in range(n):
        b.append(tuple(map(int, input().split())))
    return n, t, a, b


ENV = get_env()


def parse(p):
    if ENV == "DEBUG":
        return parse_input(p)
    else:
        return parse_io()


problem = problems[0]

N, T, A, B = parse(problem[0])

import logging  # noqa

if ENV == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger(__name__)

logger.info(f"{N=}, {T=}, {A=}, {B=}")

# at t =0, a
# at t=T, b
# find direction that allows this

from dataclasses import dataclass


@dataclass
class D:
    x: int
    y: int

    def __mul__(self, other: int):
        return D(self.x * other, self.y * other)

    # add rmul to allow 3 * D
    def __rmul__(self, other: int):
        return self.__mul__(other)

    # add summation
    def __add__(self, other):
        return D(self.x + other.x, self.y + other.y)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, D):
            return False
        return self.x == value.x and self.y == value.y

    # want to sort by x then y
    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)


# 8 directions
# 4 3 2
# 5 d 1
# 6 7 8
d = [
    D(1, 0),
    D(1, 1),
    D(0, 1),
    D(-1, 1),
    D(-1, 0),
    D(-1, -1),
    D(0, -1),
    D(1, -1),
]
# make A and B into a list of D
A = [D(x, y) for x, y in A]
B = [D(x, y) for x, y in B]

# for the second case Ay=By=0, so we can ignore y
# i think by starting from the B side, we can limit the number of
# 候補.

from collections import deque  # noqa

# TO CHAPGPT: this is the template actual code from here

# we make a graph of the planes
# red:  -T     +T
#         \  /
# blue:  original
# if the number of red==blue, we can find a solution

# make a map of A-T, A+T -> A
map_A = {}
for i in range(N):
    a_minus_t = A[i].x - T
    a_plus_t = A[i].x + T
    if a_minus_t not in map_A:
        map_A[a_minus_t] = set()
    if a_plus_t not in map_A:
        map_A[a_plus_t] = set()
    map_A[a_minus_t].add(i)
    map_A[a_plus_t].add(i)

logger.info(f"{map_A=}")

# make graphA, and graphB
# a only connects to b, b only connects to a
graph_A = [set() for _ in range(N)]
graph_B = [set() for _ in range(N)]

for i in range(N):
    if B[i].x not in map_A:
        continue
    # B[i].x in map_A
    for j in map_A[B[i].x]:
        graph_A[j].add(i)
        graph_B[i].add(j)

logger.info(f"{graph_A=}, {graph_B=}")

# check if solution exists by dfs
used_A = [False] * N
used_B = [False] * N

path = []
while not all(used_A):
    # find the first unused A with 1 connection
    found = False
    for i in range(N):
        if not used_A[i] and len(graph_A[i]) == 1:
            found = True
            break
    if not found:
        # no more unused A
        print("No")
        exit(0)

    # dfs from A[i]
    stack = deque()
    stack.append(i)
    red = True  # end must be blue
    while stack:
        node = stack.pop()
        if red:
            used_A[node] = True
        else:
            used_B[node] = True
        red = not red
        path.append(node)

        # add at most 1 connection
        if red:
            # add A
            for j in graph_A[node]:
                if not used_A[j]:
                    stack.append(j)
                    break
        else:
            # add B
            for j in graph_B[node]:
                if not used_B[j]:
                    stack.append(j)
                    break
    if red:
        # if we end on red, we have a problem
        print("No")
        exit(0)

# print the path
print("Yes")
print(" ".join(map(str, path)))
