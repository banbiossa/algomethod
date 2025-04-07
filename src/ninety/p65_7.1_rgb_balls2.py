import logging

# prod|debug
ENV = "debug"

if ENV != "prod":
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

MOD = 998244353
"""
R G B K
X Y Z
"""

problems = [
    (
        """3 1 2 5
4 2 4
""",
        2,
    ),
    (
        """65 6 12 35
30 18 35
""",
        257190020,
    ),
]

problem = problems[1]


def parse_qa(problem: str):
    lines = problem.strip().split("\n")
    R, G, B, K = map(int, lines[0].split())
    X, Y, Z = list(map(int, lines[1].split()))
    return R, G, B, K, X, Y, Z


def parse_input():
    R, G, B, K = map(int, input().split())
    X, Y, Z = list(map(int, input().split()))
    return R, G, B, K, X, Y, Z


def parse(*args):
    if ENV != "prod":
        return parse_qa(*args)
    else:
        return parse_input()


R, G, B, K, X, Y, Z = parse(problem[0])
logger.info(f"{R=}, {G=}, {B=}, {K=}, {X=}, {Y=}, {Z=}")

# r+g <= x
# r+b <= y
# g+b <= z

# the first round is r,g,b<=5 so we can brute force it
combinations = []
for r in range(min(K + 1, R + 1)):
    for g in range(min(K + 1 - r, G + 1)):
        b = K - r - g
        if b < 0 or b > B:
            continue
        if r + g > X:
            continue
        if g + b > Y:
            continue
        if b + r > Z:
            continue
        logger.info(f"found {r=}, {g=}, {b=} {r+g+b=}")
        combinations.append((r, g, b))

logger.info(f"{combinations=}")

# next step is to count the nubmer of combinations
# all the balls are distinct so it's
# comb(R, r) * comb(G, g) * comb(B, b)
if not combinations:
    print(0)
    exit(0)


def modinv(a):
    return pow(a, MOD - 2, MOD)


def comb(n, k):
    # compute n! / (k! * (n-k)!)
    # but modulo
    if k < 0 or k > n:
        return 0
    total = 1
    k = min(k, n - k)
    for i in range(k):
        total = (total * (n - i)) % MOD
        # this is division by modulo
        total = (total * modinv(i + 1)) % MOD
    return total


def tri_comb(r, g, b):
    # compute comb(R, r) * comb(G, g) * comb(B, b)
    total = 1
    total *= comb(R, r)
    total %= MOD
    total *= comb(G, g)
    total %= MOD
    total *= comb(B, b)
    total %= MOD
    return int(total)


total = 0
for r, g, b in combinations:
    temp = tri_comb(r, g, b)
    logger.info(f"{temp=} for {r=}, {g=}, {b=}")
    total += temp
    total %= MOD
logger.info(f"{total=}, ans={problem[1]}, {total == problem[1]=}")
print(total)
