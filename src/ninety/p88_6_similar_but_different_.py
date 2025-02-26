import logging
from dataclasses import dataclass
from pprint import pformat, pprint  # noqa

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


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
    return (N, Q, A, X)


qa = problems[1]
N, Q, A, X = parse_qa(qa)

logger.info(f"{N=}, {Q=}, {A=}, {X=}")

# c[t]: Y[i] = t and X[i] is used
# if c[t] >= 1, than can't use t
# keep X[i] and Y[i] in a linked list format
# (X[i] < Y[i] will always be true)
# when you choose i, c[t] += 1 for all t in linked[i]
# use xy as is, so it's a no-use indicator
