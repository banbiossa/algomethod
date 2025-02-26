import logging
from dataclasses import dataclass

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
]


def parse_qa(qa: QA) -> tuple:
    N, B, K = map(int, qa.question.split("\n")[0].split())
    c = list(map(int, qa.question.split("\n")[1].split()))
    return N, B, K, c, qa.answer


N, B, K, C, answer = parse_qa(problems[1])
logger.info(f"{N=}, {B=}, {C=}, {K=}, {answer=}")

# how many ways to get a number divisible by B
# the total number possible is K**(N**10)
# K <= 9, N <= 10^18 so this is huge
# 2 <= B <= 1000
#
# if K == 9, then N // B is the approximate answer
# so that is the upper bound

# N<=10000 and B <= 30 for the first step
# N<=10000 means MAX = 10**10000
# this probably can't be brute forced
# we look through each multiple of B and see
# if set(c) | set(b) == set(c)

# we use order dp
dp = [[0] * B for _ in range(N + 1)]
dp[0][0] = 1

for i in range(N):
    for j in range(B):
        for k in range(K):
            nex = (10 * j + C[k]) % B
            dp[i + 1][nex] += dp[i][j]
            dp[i + 1][nex] %= DIVISOR

logger.info(f"{dp=}")
print(dp[N][0])
