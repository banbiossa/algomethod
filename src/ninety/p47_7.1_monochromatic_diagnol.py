# N
# S
# T

problems = [
    (
        """5
RGBGB
GRGRB
""",
        6,
    ),
    (
        """10
BGGGRBBGRG
RGBBRGRGGG
""",
        4,
    ),
]


def parse_p(p):
    p = p.split("\n")
    N = int(p[0])
    S = p[1]
    T = p[2]
    return N, S, T


problem = problems[1]  # change here
N, S, T = parse_p(problem[0])

import logging  # noqa

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logging.info(f"N: {N}, S: {S}, T: {T}")


def add(a, b):
    # apply logic that if a==b return a
    # if not return c
    # the possible outcomes are RGB
    return {
        # for all 9 patters define a dict
        "RR": "R",
        "GG": "G",
        "BB": "B",
        "RG": "B",
        "GR": "B",
        "GB": "R",
        "RB": "G",
        "BG": "R",
        "BR": "G",
    }[a + b]


def _makestr(s, t):
    if len(s) > len(t):
        s, t = t, s
    rgb = "".join([add(s[i], t[i]) for i in range(len(s))])
    return rgb


def check(s, t) -> bool:
    # this checks if RRR, GGG will have a monotone output
    # just realized this will be O(N^3) so not sure
    rgb = _makestr(s, t)

    if len(set(rgb)) == 1:
        return True
    return False


# first is N < 2000 so a O(N^2) solution is fine
# i think a simple dp? brute force will do it
total = 0
if check(S, T):
    total += 1
for i in range(1, N):
    logger.debug(f"original {S[i:]}, {T}")
    if check(S[i:], T):
        logger.info(f"found {S[i:]}, {T}, {_makestr(S[i:], T)}")
        total += 1
for i in range(1, N):
    logger.debug(f"original {S}, {T[i:]}")
    if check(S, T[i:]):
        logger.info(f"found {S}, {T[i:]}, {_makestr(S, T[i:])}")
        total += 1
print(total)
