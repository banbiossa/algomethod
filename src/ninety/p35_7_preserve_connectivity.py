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

import sys

sys.setrecursionlimit(10**7)

# doubling + lca
# number of bits needed for doublign
bits = 0
while (1 << bits) < N:
    bits += 1

# par[i][u] will be the 2^i-th ancestor of u
par = [[0] * N for _ in range(bits)]
depth = [0] * N
id_arr = [-1] * N
vert_id = [0]


def build_tree(pos, pre):
    par[0][pos] = pre
    id_arr[pos] = vert_id[0]
    vert_id[0] += 1
    for nxt in tree[pos]:
        if nxt == pre:
            continue
        depth[nxt] = depth[pos] + 1
        build_tree(nxt, pos)


build_tree(0, -1)

# build the doubling table
for i in range(bits - 1):
    for j in range(N):
        par[i + 1][j] = par[i][par[i][j]]


def lca(va, vb):
    # ensure va is deeper
    if depth[va] < depth[vb]:
        va, vb = vb, va

    # lift va up so that depth[va] == depth[vb]
    for i in range(bits - 1, -1, -1):
        if depth[va] - depth[vb] >= (1 << i):
            va = par[i][va]
    if va == vb:
        return va

    # lift both va and vb up until their parents are equal
    for i in range(bits - 1, -1, -1):
        if par[i][va] != par[i][vb]:
            va = par[i][va]
            vb = par[i][vb]
    return par[0][va]


def dist(va, vb):
    return depth[va] + depth[vb] - 2 * depth[lca(va, vb)]


for query in V:
    sel = sorted(query, key=lambda x: id_arr[x])
    answer = 0
    for i in range(len(sel)):
        answer += dist(sel[i], sel[i - 1])
    print(answer // 2)
