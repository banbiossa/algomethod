import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""input is like
N, W
A1...AN
k1c11..c1k1
...
kNcN1..cNkN
"""

problems = (
    (
        """5 5
5 2 10 3 6
1 3
1 3
0
1 5
0""",
        2,
    ),
)
problem = problems[0]


def parse_problem(p):
    N, W = map(int, p[0].split())
    A = list(map(int, p[1].split()))
    K = []
    C = []
    for i in range(N):
        k, *c = map(int, p[i + 2].split())
        K.append(k)
        C.append(c)
    return N, W, A, K, C


N, W, A, K, C = parse_problem(problem[0].split("\n"))
logger.info(f"{N=}, {W=}, {A=}, {K=}, {C=}")


# you can pay W and get the keys in the house
# you need all keys within the house to get the money
# N <= 100 so a compute heavy solution is possible
# it's a burn or bury problem

inf = 1012345678

from dataclasses import dataclass  # noqa


@dataclass
class Edge:
    """edge in the flow network
    to: destination
    cap: capaicity = max flow
    rev: reverse edge index in destination vertex's adjacency list.
        quick access to reverse edge
    """

    to: int
    cap: int
    rev: int


def find_augment(
    pos: int,
    tar: int,
    step: int,
    G: list[list[Edge]],
    vis: list[bool],
) -> bool:
    """recursively search for augmenting path from pos to tar.
    need residual capacity >= step to pass through an edge.

    Args:
        pos (int): current
        tar (int): target
        step (int): minimum required capacity
        G (list[list[Edge]]): graph as adjacency list
        vis (list[bool]): has_been_visited

    Returns:
        bool: True if augmenting path is found
    """
    if pos == tar:
        return True
    vis[pos] = True
    for e in G[pos]:
        if not vis[e.to] and e.cap >= step:
            if find_augment(e.to, tar, step, G, vis):
                # update capacities along the path
                e.cap -= step
                G[e.to][e.rev].cap += step
                return True

    return False


def max_flow(
    src: int,
    tar: int,
    maxstep: int,
    G: list[list[Edge]],
) -> int:
    """max flow from src to tar (capacity scaling method)

    Args:
        src (int): source
        tar (int): target
        maxstep (int): capacity limit from flow to sink
        G (list[list[Edge]]): network graph

    Returns:
        int: max flow
    """
    flow = 0
    step = 1
    while step * 2 <= maxstep:
        step *= 2

    while True:
        vis: list[bool] = [False] * len(G)
        if not find_augment(src, tar, step, G, vis):
            if step == 1:
                break
            step //= 2
        else:
            flow += step
    return flow


# create graph with N+2 vertices (0: source, 1..N: nodes, N+1: sink)
G: list[list[Edge]] = [[] for _ in range(N + 2)]


def add_edge(va: int, vb: int, cap: int):
    G[va].append(Edge(vb, cap, len(G[vb])))
    G[vb].append(Edge(va, 0, len(G[va]) - 1))


# add dependency edges (1-index)
for i in range(1, N + 1):
    for c in C[i - 1]:
        add_edge(c, i, inf)

# add edges from source to nodes, node to sink
for i in range(1, N + 1):
    add_edge(0, i, A[i - 1])
    add_edge(i, N + 1, W)

# compute max flow
res = max_flow(0, N + 1, W, G)
answer = sum(A) - res
print(answer)
