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
    (
        """23502 65936 72385 95835
72759 85735 72385""",
        229429276,
    ),
]

problem = problems[2]


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


def modinv(a):
    return pow(a, MOD - 2, MOD)


# we can precompute the factorials and inverse factorials
fact = [1]
for i in range(max(R, G, B)):
    fact.append(fact[-1] * (i + 1) % MOD)
inv = []
for i in range(max(R, G, B) + 1):
    inv.append(modinv(fact[i]))


def comb(n, k):
    # compute n! / (k! * (n-k)!)
    # but modulo
    if k < 0 or k > n:
        return 0
    total = fact[n]
    total *= inv[k]
    total %= MOD
    total *= inv[n - k]
    total %= MOD
    return int(total)


# r+g <= x
# r+b <= y
# g+b <= z

# because r+g+b == K
# the above also emplies that
# b >= K - x
# r >= K - y
# g >= K - z

# now we have r,g,b with a lower and upper bound of
# K-y <= r <= R
# K-z <= g <= G
# K-x <= b <= B

# let's define the xCy = (x, y) number as below
# r_i = (R, i) if i in [K-y, R] else 0
# g_i = (G, i) if i in [K-z, G] else 0
# b_i = (B, i) if i in [K-x, B] else 0

# using this the answer is written as
# Ans =
# sum over i (0 <= i <= R)
#   sum over j (0 <= j <= G)
#     r_i * g_j * b_(K-i-j)

# we now think of dx, the convolution of r,g
# d_x = conv(r, g, x)
# meaning that for all i,j where i+j == X
# d_X is defined as sum(r_i * g_j)

# the answer is then
# Ans =
#   sum over i (0 <= i <= K)
#      d_i * b_(K-i)

# the convolution d_0, ..., d_2K can be computed
# by FFT in O(N log N) time so faster than O(N^2)

# we will now code this step by step

# first get r,g,b
r = [0] * (max(R, G, B, K) + 1)
g = [0] * (max(R, G, B, K) + 1)
b = [0] * (max(R, G, B, K) + 1)

for i in range(K - Y, R + 1):
    r[i] = comb(R, i)
for i in range(K - Z, G + 1):
    g[i] = comb(G, i)
for i in range(K - X, B + 1):
    b[i] = comb(B, i)


def ntt(a, mod, root):
    """In-place NTT (Number Theoretic Transform) on list a."""
    n = len(a)
    # Bit-reversal permutation
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j -= bit
            bit //= 2
        j += bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    # Cooley-Tukey iterative NTT
    length = 2
    while length <= n:
        # Compute the primitive root of unity for this stage
        wlen = pow(root, (mod - 1) // length, mod)
        for i in range(0, n, length):
            w = 1
            for j in range(i, i + length // 2):
                u = a[j]
                v = a[j + length // 2] * w % mod
                a[j] = (u + v) % mod
                a[j + length // 2] = (u - v) % mod
                w = w * wlen % mod
        length *= 2
    return a


def intt(a, mod, inv_root):
    """In-place inverse NTT on list a using the inverse primitive root."""
    n = len(a)
    # Bit-reversal permutation (same as in ntt)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j -= bit
            bit //= 2
        j += bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    # Inverse transform: similar structure, but using inv_root
    length = 2
    while length <= n:
        wlen = pow(inv_root, (mod - 1) // length, mod)
        for i in range(0, n, length):
            w = 1
            for j in range(i, i + length // 2):
                u = a[j]
                v = a[j + length // 2] * w % mod
                a[j] = (u + v) % mod
                a[j + length // 2] = (u - v) % mod
                w = w * wlen % mod
        length *= 2
    # Normalize by multiplying with modular inverse of n
    n_inv = pow(n, mod - 2, mod)
    for i in range(n):
        a[i] = a[i] * n_inv % mod
    return a


def fft_convolve_mod(a, b, mod=998244353, root=3):
    """
    Convolve two integer lists a and b modulo mod using NTT.
    Both a and b are lists of integers.
    """
    # Determine the size of convolution:
    n = 1
    total_length = len(a) + len(b) - 1
    while n < total_length:
        n *= 2

    # Pad the lists with zeros up to length n
    A = a + [0] * (n - len(a))
    B = b + [0] * (n - len(b))

    # Compute the forward NTT for both
    ntt(A, mod, root)
    ntt(B, mod, root)

    # Pointwise multiplication
    C = [(A[i] * B[i]) % mod for i in range(n)]

    # Compute the inverse NTT; inv_root is the modular inverse of root modulo mod
    inv_root = pow(root, mod - 2, mod)
    intt(C, mod, inv_root)

    # Return the convolution result of the proper length
    return C[:total_length]


# next we need to compute the convolution

# we need to use fftconv
d = fft_convolve_mod(r, g)
logger.info(d)

# we get the final output by sum(d_i * b_(K-i))
total = 0
for i in range(K + 1):
    total += d[i] * b[K - i]
    total %= MOD
print(total)
logger.info(f"{total=}, {problem[1]=}, {total == problem[1]=}")
