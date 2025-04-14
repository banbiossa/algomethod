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

# for the first case N<=6 so i think brute force
# each plane has 8 possible destinations
# so 8**6 = 2**18 < 10**6 so yeah

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

for i in range(8**N):
    # we need to parse this into N digits of 8
    # so in base 2, e.g., 000-001-010-011-100-101-110-111
    str_i_base2 = str(bin(i))[2:].zfill(N * 3)
    # we keep this in a array of N digits
    i_arr = [str_i_base2[j : j + 3] for j in range(0, len(str_i_base2), 3)]
    # we convert this binary str to a list of ints, so 010 -> 2 etc.
    i_ints = [int(n, 2) for n in i_arr]

    # we now check whether this is a valid solution
    # for now we check if a[i] + d[i_ints[i]] == b[i]
    # we sort because the order of the planes does not matter
    left = [A[j] + T * d[i_ints[j]] for j in range(N)]
    if sorted(left) == sorted(B):
        logger.info("found a solution")
        print("Yes")
        print(" ".join([str(i_ints[j] + 1) for j in range(N)]))
        exit(0)

print("No")
