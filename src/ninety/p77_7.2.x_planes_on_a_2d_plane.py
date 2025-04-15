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


@dataclass
class Candidate:
    n: int  # index
    d: int  # direction
    direction: list  # keeps track of A side planes directions

    def __post_init__(self):
        self.plane = B[self.n]

    @property
    def dt(self):
        # the destination of the candidate
        return self.plane.x + self.d * T


# we keep the que
que = deque(
    [
        Candidate(0, -1, [None] * N),
        Candidate(0, 1, [None] * N),
    ],
)

# our basic idea is to start from the B side (1 to N)
# then go 1 to N and check if there is a corresponding A side
# we will go depth first by que.appendleft and que.popleft
while que:
    c = que.popleft()

    # we find the destination of the candidate
    found = False
    for i in range(N):  # loop through the A planes
        if c.direction[i] is not None:  # skip if plane A[i] is already set
            continue
        # if we find one, we use that
        # even if there are multiple, we can just use the first one
        # because the order of the planes does not matter
        if c.dt == A[i].x:
            found = True
            c.direction[i] = c.d  # save the direction
            break

    if not found:
        continue

    # but if already c.n == N-1, we are done
    # the answer is the direction of the A planes
    # so we print that (and save that later)
    if c.n == N - 1:
        # we have found a solution
        logger.info("found a solution")
        print("Yes")
        # print the direction saved for the A planes
        # we need to map the direction to 1-8
        x_to_8 = {1: "5", -1: "1"}  # the direction is reversed
        print(" ".join([x_to_8[c.direction[i]] for i in range(N)]))
        exit(0)

    # we found a candidate, so we add n+1 to the que
    new_direction = c.direction.copy()
    # add -1 and 1 to the que
    que.appendleft(Candidate(c.n + 1, -1, new_direction.copy()))
    que.appendleft(Candidate(c.n + 1, 1, new_direction.copy()))

print("No")
