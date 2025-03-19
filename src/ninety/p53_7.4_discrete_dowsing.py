import random  # noqa
from dataclasses import dataclass
import logging

RMAX = 1500
SEED = 12
ENV = "prod"

logging.basicConfig(level=logging.DEBUG)
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

    @classmethod
    def clear(cls):
        cls.counter = 0
        cls.cache = {}

    @classmethod
    def query(cls, n: int) -> int:
        cls.counter += 1
        if ENV == "dev":
            return unrandom_array(SEED, RMAX)[0][n]

        # cache hit
        if n in cls.cache:
            return cls.cache[n]

        # no cache
        # 1-index
        print(f"? {n + 1}")
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


problem, N, A = unrandom_array(SEED)
logger.info(f"{N=}, {A=}")
logger.debug(f"{problem=}")

# logger.debug(f"{query(0)=}")


def get_t():
    if ENV != "dev":
        return int(input())
    else:
        logger.info("T=2 for test")
        return 2


def get_n():
    if ENV != "dev":
        return int(input())
    else:
        logger.info(f"N={N}")
        global SEED
        SEED += 1
        return N


T = get_t()

for _ in range(T):
    Query.clear()
    N = get_n()

    ans = 0
    cl = 0
    cr = N - 1

    # use binary search with df/dx
    for i in range(11):
        cm = (cl + cr) // 2

        d1 = P(cm)
        ans = max(ans, d1.a)
        # break for smaller N
        if cm + 1 >= N:
            break

        d2 = P(cm + 1)
        ans = max(ans, d2.a)

        if d1 < d2:
            cl = cm
        else:
            cr = cm

    print(f"! {ans}")
