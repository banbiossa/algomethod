import logging

"""
N M Q
X1 Y1
...
XM YM
A1 B1
...
AQ BQ
"""


problems = [
    (
        """6 6 3
1 3
2 4
1 4
4 6
5 6
1 5
2 6
1 5
3 6""",
        """Yes
Yes
No""",
    ),
]


problem = problems[0]

ENV = "dev"
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def parse_qa(problem: str) -> tuple:
    N, M, Q = map(int, problem.split("\n")[0].split())
    XY = [tuple(map(int, x.split())) for x in problem.split("\n")[1 : M + 1]]
    AB = [tuple(map(int, x.split())) for x in problem.split("\n")[M + 1 : M + Q + 1]]
    return N, M, Q, XY, AB


def parse_input() -> tuple:
    N, M, Q = map(int, input().split())
    XY = [tuple(map(int, input().split())) for _ in range(M)]
    AB = [tuple(map(int, input().split())) for _ in range(Q)]
    return N, M, Q, XY, AB


def parse() -> tuple:
    if ENV == "prod":
        return parse_input()

    return parse_qa(problem[0])


N, M, Q, XY, AB = parse()

logger.info(f"{N=}, {M=}, {Q=}, {XY=}, {AB=}")

# make xy 0-indexed and as a list of edges
xy = [[] for _ in range(N)]
for x, y in XY:
    xy[x - 1].append(y - 1)

# make the query 0-indexed
ab = [(a - 1, b - 1) for a, b in AB]

logger.info(f"{xy=}, {ab=}")

# the dumb option is to do a BFS for each query
from collections import deque  # noqa

for a, b in ab:
    logger.info(f"{a=}, {b=}")
    q = deque()
    q.append(a)
    visited = [False] * N
    while q:
        logger.debug(f"{q=}")
        x = q.popleft()
        if x == b:
            print("Yes")
            break
        if visited[x]:
            continue
        visited[x] = True
        logger.debug(f"{xy[x]=}")
        for y in xy[x]:
            q.append(y)
    else:
        print("No")
