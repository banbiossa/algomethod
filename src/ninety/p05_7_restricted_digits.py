import logging
from dataclasses import dataclass
from math import log2

logging.basicConfig(level=logging.DEBUG)
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


N, B, K, C, answer = parse_qa(problems[1])
logger.info(f"{N=}, {B=}, {K=}, {C=}, {answer=}")

IMAX = int(log2(N)) + 1

power10 = [10 % B]
for _ in range(IMAX - 1):
    power10.append((power10[-1] ** 2) % B)

logger.info(f"{power10=}")


# this is dp[2**i][j] in that sense
dp = [[0] * B for _ in range(IMAX + 1)]

# compute the 1st (2**0) row
for k in range(K):
    nex = C[k] % B
    dp[0][nex] += 1

# iteratively compute the power(2) rows
for i in range(IMAX):
    for j in range(B):
        for k in range(B):
            nex = (j * power10[i] + k) % B
            dp[i + 1][nex] += dp[i][j] * dp[i][k]
            dp[i + 1][nex] %= DIVISOR
# logger.info(f"{np.array(dp)=}")

# now we have dp[1], dp[2], dp[4], ...
# we need to get dp[N][0] from here

# we did doubling by dp[2**i] = dp[2**(i-1)] * dp[2**(i-1)]
# this means we can dp[i] = sum_over_k (dp[j] + dp[i-j])
# so with the iterative power of 2 analogy, we can do the same

calc = [0] * B
calc[0] = 1
for i in range(IMAX):
    if not (N >> i) & 1:
        logger.debug(f"skip {i=}")
        continue

    logger.debug(f"add {i=}")
    calc_next = [0] * B
    for j in range(B):
        for k in range(B):
            nex = (k * power10[i] + j) % B
            calc_next[nex] += dp[i][j] * calc[k]
            calc_next[nex] %= DIVISOR

    calc = calc_next


print(calc)
print(calc[0])
