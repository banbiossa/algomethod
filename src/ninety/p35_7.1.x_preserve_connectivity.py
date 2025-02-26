import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""problem comes in like
N
A1 B1
A2 B2
AN-1 BN-1
Q
K1 V11 V12 ... V1K1
...
KQ VQ1 VQ2 ... VQKQ
"""

problems = [
    (
        """6
1 2
2 3
3 4
1 5
3 6
5
2 1 2
3 1 3 5
4 2 3 4 5
5 1 2 3 5 6
6 1 2 3 4 5 6
""",
        """1
3
4
4
5""",
    ),
    (
        """6
1 2
2 3
3 4
1 5
3 6
5
2 1 2
2 3 4
2 4 6
2 1 5
2 2 5
""",
        """1
1
2
1
2
""",
    ),
]

problem = problems[1]


def parse_problem(p):
    p = p.strip().split("\n")
    N = int(p[0])
    AB = []
    for i in range(N - 1):
        a, b = map(int, p[i + 1].split())
        AB.append((a, b))
    Q = int(p[N])
    K = []
    V = []
    for i in range(Q):
        k, *v = map(int, p[N + i + 1].split())
        K.append(k)
        # 0-index v
        v = [x - 1 for x in v]
        V.append(v)

    return N, AB, Q, K, V


N, AB, Q, K, V = parse_problem(problem[0])
logger.debug(f"{N=}, {AB=}, {Q=}, {K=}, {V=}")

# first we think where N,Q <= 5000
# so we can try NQ solution
# the answer is tree dp
# for each node, we count the number of colored nodes
# in the subtree. if it is between 1 and K-1 we count it
# this will count all nodes so it costs O(N) thus is the answer

# make tree from AB
tree = [[] for _ in range(N)]
for a, b in AB:
    a -= 1
    b -= 1
    tree[a].append(b)
    tree[b].append(a)


for sel in V:
    c = [0] * N
    for x in sel:
        c[x] += 1

    def tree_dp(pos, parent):
        for child in tree[pos]:
            if child == parent:
                continue
            tree_dp(child, pos)
            c[pos] += c[child]

    tree_dp(sel[0], -1)

    need = sum(1 for i in range(N) if i != sel[0] and c[i] != 0)
    print(need)
