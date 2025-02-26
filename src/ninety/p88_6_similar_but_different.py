import logging
from dataclasses import dataclass
from typing import Optional  # noqa

logging.basicConfig(level=logging.INFO)


@dataclass
class QA:
    q: str
    a: str


problems: list[QA] = [
    QA(
        q="""5 2
3 1 3 2 3
1 2
1 4""",
        a="""4
2 3 4 5
3
1 3 5
""",
    ),
    QA(
        q="""10 10
2 5 7 8 11 10 1 88 86 50
1 2
1 3
1 4
1 5
1 6
5 10
6 10
2 3
9 10
7 8
""",
        a="""2
6 7
1
5
""",
    ),
]

# parse a problem into
# N Q
# A1 A2 ... AN
# X1 X2
# ...
# XQ XQ


def parse_qa(qa: QA) -> tuple[int, int, list[int], list[list[int]]]:
    lines = qa.q.strip().split("\n")
    N, Q = map(int, lines[0].split())
    A = list(map(int, lines[1].split()))
    X = [list(map(int, line.split())) for line in lines[2:]]
    # make X 0-indexed
    X0 = []
    for x in X:
        X0.append([i - 1 for i in x])
    return (N, Q, A, X0)


qa = problems[0]
N, Q, A, X = parse_qa(qa)

logger = logging.getLogger()
logger.info(f"{N=}, {Q=}, {A=}, {X=}")

# c[t]: Y[i] = t and X[i] is used
# if c[t] >= 1, than can't use t
# keep X[i] and Y[i] in a linked list format
# (X[i] < Y[i] will always be true)
# when you choose i, c[t] += 1 for all t in linked[i]
# use xy as is, so it's a no-use indicator

# as a linked list format
linked = [set() for _ in range(N)]
for i in range(Q):
    a, b = X[i]
    linked[a].add(b)
    linked[b].add(a)

logger.info(f"{linked=}")

# c = [0] * (N + 1)

# make the cuckoo's nest
# 鳩の巣論法用の巣穴の用意
# ここで被ったら、そこをリプレイする？
cuckoo = [-1] * (sum(A) + 1)


def dfs(i, path, c):
    # will return truthy if 2 values are found
    logger.info(f"{i=}, {path=}, {c=}")
    if i >= N:
        logger.info(f"{i=}, {N=}")
        # all done
        total = sum([A[i] for i in path])
        if cuckoo[total] != -1 and total != 0:
            logger.info(f"{cuckoo[total]=}, {total=}, {i=}")
            return cuckoo[total], path
        cuckoo[total] = path
        return

    # not use
    c2 = c.copy()
    paths = dfs(i + 1, path, c2)
    if paths:
        return paths

    # check if can use
    if c[i] >= 1:
        logger.info(f"skipping {c[i]=}, {i=}")
        return

    # use
    c1 = c.copy()
    for j in linked[i]:
        c1[j] += 1
    paths = dfs(i + 1, path + [i], c1)
    if paths:
        return paths


paths = dfs(0, [], [0] * N)
logger.info(f"{paths=}")

assert paths
# print as i indexed
for path in paths:
    print(len(path))
    print(" ".join([str(i + 1) for i in path]))
