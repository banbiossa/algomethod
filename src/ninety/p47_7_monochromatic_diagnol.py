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

logger.info(f"N: {N}, S: {S}, T: {T}")


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


# we use rolling hash for the general cas6

# part1
# 1 <= N <= 10^6 so we need a O(N) solution
# for t, if we want R we flip G to B and B to G
#
# original
# s: R G B
# t: R B G
# =: R R R
#
# flipped
# s: R G B
# t: R G B
# =: R R R
#
# we can see now that s==t, so this is the condition

# part2: find a fast way to find s==t
# k < 0: s[-k+1]s[-k+2]...s[n] == t[1]t[2]...t[n+k]
# k >=0: s[1]s[2]...s[n-k] == t[k+1]t[k+2]...t[n]

# rolling hash
# hash(X) = (b^(L-1)*X[0] + b^(L-2)*X[1] + ... + b^0*X[L-1]) mod p
# p is prime, X is a number
# h[0] = 0, h[k] = (b*h[k-1] + X[k]) mod p
# s[l]s[l+1]...s[r-1] = (h[r] - b^(r-l)*h[l]) mod p
mod = 699999953  # large prime

# make s and t into 0,1,2
mapping = {"R": 0, "G": 1, "B": 2}
seq1 = [mapping[i] for i in S]
seq3 = [mapping[i] for i in T]

logger.info(f"{seq1=}, {seq3=}")

answer = 0
# calculate for r,g,b
for i in range(3):
    seq2 = [0] * N
    for j in range(N):
        # this is a smart flip,
        # when i=0 -> R
        # R = 0 = 0 - 0 + 3 = 3 % 3 = 0 = R
        # G = 1 = 0 - 1 + 3 = 2 % 3 = 2 = B  <- flipped
        # B = 2 = 0 - 2 + 3 = 1 % 3 = 1 = G  <- flipped
        # when i=1 -> G
        # R = 0 = 2 - 0 + 3 = 5 % 3 = 2 = B  <- flipped
        # G = 1 = 2 - 1 + 3 = 4 % 3 = 1 = G
        # B = 2 = 2 - 2 + 3 = 3 % 3 = 0 = R  <- flipped
        # when i = 2 -> B
        # R = 0 = 4 - 0 + 3 = 7 % 3 = 1 = G  <- flipped
        # G = 1 = 4 - 1 + 3 = 6 % 3 = 0 = R  <- flipped
        # B = 2 = 4 - 2 + 3 = 5 % 3 = 2 = B
        seq2[j] = (i * 2 - seq3[j] + 3) % 3

    # calcuate the rolling hash
    # as previously mentioned
    # k < 0: s[-k+1]s[-k+2]...s[n] == t[1]t[2]...t[n+k]
    # k >=0: s[1]s[2]...s[n-k] == t[k+1]t[k+2]...t[n]

    # rolling hash
    # hash(X) = (b^(L-1)*X[0] + b^(L-2)*X[1] + ... + b^0*X[L-1]) mod p
    # h[0] = 0, h[k] = (b*h[k-1] + X[k]) mod p
    # s[l]s[l+1]...s[r-1] = (h[r] - b^(r-l)*h[l]) mod p

    # k >=0: s[1]s[2]...s[n-k] == t[k+1]t[k+2]...t[n]
    # we build the hash from the bottom left
    # so head of s and tail of k
    power3 = 1
    hash1 = 0
    hash2 = 0
    for k in range(N):
        # build s from head
        hash1 = (3 * hash1 + seq1[k]) % mod
        # build t from tail (so "lift" the seq2 up by power3)
        hash2 = (hash2 + power3 * seq2[N - k - 1]) % mod
        if hash1 == hash2:
            answer += 1
        power3 = (power3 * 3) % mod

    # k < 0: s[-k+1]s[-k+2]...s[n] == t[1]t[2]...t[n+k]
    power3 = 1
    hash1 = 0
    hash2 = 0
    for k in range(N - 1):
        hash1 = (hash1 + power3 * seq1[N - k - 1]) % mod
        hash2 = (3 * hash2 + seq2[k]) % mod
        if hash1 == hash2:
            answer += 1
        power3 = (power3 * 3) % mod

print(answer)
