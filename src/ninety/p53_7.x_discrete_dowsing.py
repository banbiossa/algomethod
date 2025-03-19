import random  # noqa
from dataclasses import dataclass
import logging

RMAX = 1500
SEED = 12
ENV = "prod"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class P:
    n: int
    a: int

    def __init__(self, n: int):
        self.n = n
        self.a = query(n)

    def __lt__(self, other):
        return self.a < other.a


def query(n: int) -> int:
    if ENV != "debug":
        # 1-index
        print(f"? {n + 1}")
        ans = int(input())
        return ans
    else:
        counter[0] += 1
        return unrandom_array(SEED, RMAX)[0][n]


counter = [0]


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


def new_candidate(a: P, b: P) -> P:
    # find the middle
    middle = (a.n + b.n) // 2
    return P(middle)


def add_candidates(candidates: list[P]) -> list[P]:
    # will get 3 points, add candidates between the 3 points
    # if the difference is 1, then we can't add a candidate
    if candidates[1].n - candidates[0].n > 1:
        left = new_candidate(candidates[0], candidates[1])
        candidates.insert(1, left)
        logger.debug(f"{left=}")
    # check the last 2 elements
    if candidates[-1].n - candidates[-2].n > 1:
        right = new_candidate(candidates[-1], candidates[-2])
        candidates.insert(-1, right)
        logger.debug(f"{right=}")
    return candidates


def get_t():
    if ENV == "debug":
        T = 2
    else:
        T = int(input())
    return T


def get_n():
    if ENV == "debug":
        N = RMAX
    else:
        N = int(input())
    return N


T = get_t()
for _ in range(T):
    N = get_n()
    RMAX = N

    # greedy for small N
    if N < 15:
        points = [P(i) for i in range(N)]
        print(f"! {max(points).a}")
        continue

    # start with 3 points
    left_edge = 0
    right_edge = RMAX
    candidates = [P(left_edge), P(right_edge // 2), P(right_edge - 1)]
    logger.info(f"{candidates=}")
    while True:
        # add points between the 3 points
        candidates = add_candidates(candidates)
        logger.debug(f"{candidates=}")

        # break if none were added
        if len(candidates) == 3:
            logger.info(f"end of loop {candidates=}")
            break

        # some can be removed
        # the max will always be close to the current max
        # so the range of interest will always be [i_argmax - 1, i_argmax + 1]

        # get the argmax and index
        argmax = max(candidates)
        index = candidates.index(argmax)

        # always keep 3 points
        if index == 0:
            candidates = candidates[: index + 2]
        elif index == len(candidates) - 1:
            candidates = candidates[index - 1 :]
        else:
            candidates = candidates[index - 1 : index + 2]

        assert len(candidates) == 3

    # the argmax is the answer
    print(f"! {argmax.a}")

    logger.info(f"{counter=}")
