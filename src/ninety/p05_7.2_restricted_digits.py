import logging
from dataclasses import dataclass

import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

DIVISOR = 10**9 + 7


@dataclass
class QA:
    question: str
    answer: int


problems = [
    QA(
        question="""3 7 3
1 4 9""",
        answer=3,
    ),
    QA(
        question="""5 2 3
1 4 9
""",
        answer=81,
    ),
    QA(
        question="""10000 27 7
1 3 4 6 7 8 9
""",
        answer=989112238,
    ),
    QA(
        question="""1000000000000000000 29 6
1 2 4 5 7 9""",
        answer=853993813,
    ),
]


def parse_qa(qa: QA) -> tuple:
    N, B, K = map(int, qa.question.split("\n")[0].split())
    c = list(map(int, qa.question.split("\n")[1].split()))
    return N, B, K, c, qa.answer


N, B, K, C, answer = parse_qa(problems[2])
logger.info(f"{N=}, {B=}, {K=}, {C=}, {answer=}")

# use matrix multiplication
A = [[0] * B for _ in range(B)]
for i in range(B):
    for k in range(K):
        nex = (10 * i + C[k]) % B
        # A[nex][i] += 1
        A[i][nex] += 1

A = np.array(A, dtype=np.int64)
M = np.eye(B, dtype=np.int64)

logger.info(f"{A=}")


def mul(mA, mB):
    mC = np.zeros_like(mA)
    for i in range(B):
        for j in range(B):
            for k in range(B):
                mC[i][j] += mA[i][k] * mB[k][j]
                mC[i][j] %= DIVISOR
    return mC


# iteritively multiply A by itself
logger.info(f"{N=}, {np.log2(N)=}")
logger.info(f"{bin(N)=}")
for i in range(int(np.log2(N)) + 1):
    logger.debug(f"{i=}")
    if (N >> i) & 1:
        logger.info(f"multiply {i=}")
        M = mul(M, A)
        logger.debug(f"{M=}")

    A = mul(A, A)
    logger.debug(f"{A=}")

logger.info(f"{M=}")
print(M[0][0])
