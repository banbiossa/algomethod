from dataclasses import dataclass


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
    # 1-index
    print(f"? {n + 1}")
    ans = int(input())
    return ans


T = int(input())
for _ in range(T):
    N = int(input())

    # use 3 splitting
    # for l and r, (l+l+r)//3 and (l+r+r)//3
    l = 0
    r = N - 1

    while r - l > 2:
        m1 = (l + l + r) // 3
        m2 = (l + r + r) // 3

        p1 = P(m1)
        p2 = P(m2)

        if p1 < p2:
            l = m1
        else:
            r = m2

    mid = P((l + r) // 2)
    print(max(P(l), mid, P(r)).n + 1)
