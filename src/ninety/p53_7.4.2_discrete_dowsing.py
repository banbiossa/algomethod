import random  # noqa
from dataclasses import dataclass
import logging

RMAX = 1500
SEED = 12
ENV = "dev"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class P:
    n: int
    a: int

    def __init__(self, n: int):
        self.n = n
        self.a = Query.query(n)

    def __lt__(self, other):
        return self.a < other.a

    def __repr__(self):
        return f"P(n={self.n:,}, a={self.a:_})"


class Query:
    counter = 0
    cache = {}
    N: int

    @classmethod
    def clear(cls, N):
        cls.counter = 0
        cls.cache = {}
        cls.N = N

    @classmethod
    def query(cls, n: int) -> int:
        # we pad up to 1537, so for large N, we return -n
        # this nudges the search to the left, while being valid
        if n >= cls.N:
            logger.debug(f"n={n} >= N={cls.N}")
            return -n

        # cache hit
        if n in cls.cache:
            logger.debug(f"cache hit {n=}, {cls.cache[n]=}")
            return cls.cache[n]

        cls.counter += 1
        if ENV == "dev":
            ans = unrandom_array(SEED, RMAX)[0][n]
            cls.cache[n] = ans
            return ans

        # no cache
        # 1-index
        logger.debug(f"no cache query {n=}")
        print(f"? {n + 1}", flush=True)
        ans = int(input())
        cls.cache[n] = ans
        return ans


# to make a better mock (simulation), we will do the following
# make a random answer (N, A) which will be the max
# make a list of [0, 1, 2, ..., N-1] and [N, N+1, N+2, ..., NMAX]
# and sort in ascending order + decreasing order
# seed this to make this non-random
def unrandom_array(seed: int = SEED, size=RMAX) -> tuple[list[int], int, int]:
    random.seed(seed)
    N = random.randint(1, size)
    A = random.randint(10**3, 10**9)

    # randomly sample N-1 numbers from [0, A-1]
    left = random.sample(range(A), N - 1)
    left.sort()
    # random sample NMAX-N numbers from [0, A-1]
    right = random.sample(range(A), size - N)
    right.sort(reverse=True)

    combined = left + [A] + right
    assert len(combined) == size
    return combined, N, A


# logger.debug(f"{query(0)=}")


def get_t():
    if ENV != "dev":
        return int(input())
    else:
        T = 10
        logger.info(f"{T=} for test")
        return T


def get_n():
    if ENV != "dev":
        return int(input())
    else:
        logger.info(f"N={RMAX}")
        global SEED
        SEED += 1
        return RMAX


T = get_t()

for _ in range(T):
    N = get_n()
    Query.clear(N)

    problem, Nmax, A = unrandom_array(SEED)
    logger.info(f"{Nmax=}, {A=}")
    logger.debug(f"{problem=}")

    # trivial case
    if N == 1:
        ans = P(0)
        print(f"! {ans.a}", flush=True)
        continue

    # get fibonacci number that goes over N
    fib = [1, 1]
    while fib[-1] < N:
        fib.append(fib[-1] + fib[-2])
    F = fib[-1]

    cl = 0
    cr = F - 1

    # golden ratio search
    while cr - cl > 2:
        # golden ratio
        d1 = cl + (cr - cl) * 0.382
        d2 = cl + (cr - cl) * 0.618

        # this should be close to a round number
        logger.debug(f"{cl=}, {cr=}, {d1=}, {d2=}")
        d1 = round(d1)
        d2 = round(d2)
        p1 = P(d1)
        p2 = P(d2)

        logger.debug(f"{p1=}, {p2=}")

        # cl, d1, d2, cr
        if p1 > p2:
            cr = d2
        else:
            cl = d1

    # cl-cr dist should be 2 so check
    # cl, (cl+cr)//2, cr
    ans = max(P(cl), P((cl + cr) // 2), P(cr))

    print(f"! {ans.a}", flush=True)
    logger.info(f"{Query.counter=}")
