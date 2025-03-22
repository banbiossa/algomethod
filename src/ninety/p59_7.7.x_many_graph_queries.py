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
    if ENV == "dev":
        return parse_qa(problem[0])
    return parse_input()


N, M, Q, XY, AB = parse()

logger.info(f"{N=}, {M=}, {Q=}, {XY=}, {AB=}")

# make xy 0-indexed and as a list of edges
xy = [[] for _ in range(N)]
for x, y in XY:
    xy[y - 1].append(x - 1)

# make the query 0-indexed
ab = [(a - 1, b - 1) for a, b in AB]

logger.info(f"{xy=}, {ab=}")

from itertools import islice  # noqa


def batched(iterable, n):
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


# let's use dags
# let's calculate 64 queries at a time
# (this will be a 64 time speedup)
for abab in batched(ab, 64):
    # parse abab into aa and bb
    aa, bb = zip(*abab)

    # dp[v]: クエリq(0<k<=63)において、頂点s_qから頂点vに
    # 到達可能な時だけ２進法の2^qの位を１にした値
    dp = [0] * N
    # each value of dp is a number from 1 to 1<<64
    # 最初dp[v]をs_q=vとなる2^qの総和として初期化
    for i, v in enumerate(aa):
        dp[v] |= 1 << i  # flip the i-th value to 1

    for v in range(N):
        # logger.debug(f"{v=}, {xy[v]=}, {dp=}")
        for a in xy[v]:
            dp[v] |= dp[a]

    # print the answers for the batch
    for i, b in enumerate(bb):
        if (dp[b] >> i) & 1:
            print("Yes")
        else:
            print("No")
