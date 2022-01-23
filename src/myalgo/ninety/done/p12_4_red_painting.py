def test_main():
    inputs = [
        """3 3
10
1 2 2
1 1 1
2 1 1 2 2
1 3 2
2 1 1 2 2
2 2 2 3 2
1 2 3
1 2 1
2 1 1 2 2
2 1 1 3 3
""",
        """1 1
3
2 1 1 1 1
1 1 1
2 1 1 1 1
""",
        """5 5
42
2 3 4 3 4
2 3 2 3 2
1 4 1
2 4 1 2 2
1 1 2
1 4 5
1 3 3
2 4 2 1 3
1 3 5
2 2 4 2 3
2 2 4 2 5
2 3 4 5 1
2 3 1 2 2
2 3 1 1 2
2 2 4 5 2
2 3 2 5 3
1 4 3
2 3 3 3 5
2 3 1 3 2
1 1 5
2 4 4 5 3
1 1 4
2 1 3 2 5
2 4 3 1 4
2 2 3 3 3
1 2 1
1 2 5
2 1 4 5 3
2 4 4 2 5
2 4 2 2 4
1 2 2
2 4 1 5 2
1 2 4
2 3 1 4 1
1 4 4
2 3 2 2 1
2 1 1 5 2
1 4 2
2 4 2 3 5
1 3 2
1 3 4
1 2 3
""",
    ]
    answers = [
        """No
No
Yes
Yes
No
""",
        """No
Yes
""",
        """No
No
No
No
No
No
No
No
No
No
No
No
No
No
No
No
No
No
No
No
No
No
No
No
Yes
""",
    ]
    for text, answer in zip(inputs, answers):
        H, W = map(int, text.splitlines()[0].split())
        Q = int(text.splitlines()[1])
        queries = []
        for q in range(Q):
            # index to 0
            queries.append(
                list(map(lambda x: int(x) - 1, text.splitlines()[q + 2].split()))
            )
        assert main(H, W, Q, queries) == answer.splitlines()

        # class version
        r = RedPainting(H, W)
        assert r.solve(queries) == answer.splitlines()

        # using UnionFind
        u = UnionFind(H, W)
        assert u.solve(queries) == answer.splitlines()


class UnionFind:
    def __init__(self, H, W):
        self.H = H
        self.W = W
        self.par = [-1] * (H * W)
        self.grid = [0] * (H * W)
        self.height = [0] * (H * W)

    def index(self, r, c):
        return r * self.W + c

    def root(self, x):
        if self.par[x] == -1:
            return x
        self.par[x] = self.root(self.par[x])
        return self.par[x]

    def is_same(self, ra, ca, rb, cb):
        a = self.index(ra, ca)
        b = self.index(rb, cb)
        if not (self.grid[a] and self.grid[b]):
            return False
        return self.root(a) == self.root(b)

    def join(self, x, y):
        rx, ry = self.root(x), self.root(y)
        if rx == ry:
            return False
        # force rx > ry
        if self.height[rx] < self.height[ry]:
            rx, ry = ry, rx
        self.par[rx] = ry
        if self.height[rx] == self.height[ry]:
            self.height[ry] += 1
        return True

    def paint(self, r, c):
        """(r, c) を赤く塗る"""
        current = self.index(r, c)
        self.grid[current] = 1
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            adjacent = self.index(r + dx, c + dy)
            if (0 <= adjacent < self.H * self.W) and self.grid[adjacent]:
                self.join(current, adjacent)

    def solve(self, queries):
        ans = []
        for q in queries:
            if q[0] == 0:
                _, r, c = q
                self.paint(r, c)
            if q[0] == 1:
                _, ra, ca, rb, cb = q
                if self.is_same(ra, ca, rb, cb):
                    ans.append("Yes")
                    # print("Yes")
                else:
                    ans.append("No")
                    # print("No")
        return ans


class RedPainting:
    def __init__(self, H, W):
        self.H = H
        self.W = W
        self.islands = []

    def solve(self, queries):
        ans = []
        for q in queries:
            if q[0] == 0:
                _, r, c = q
                self.add_island(r, c)
            if q[0] == 1:
                _, ra, ca, rb, cb = q
                if self.is_same(ra, ca, rb, cb):
                    ans.append("Yes")
                    # print("Yes")
                else:
                    ans.append("No")
                    # print("No")
        return ans

    def is_same(self, ra, ca, rb, cb) -> bool:
        """同じ島にいるかどうか"""
        for island in self.islands:
            if (ra, ca) in island:
                if (rb, cb) in island:
                    return True
                return False
        return False

    def add_island(self, r, c):
        # add to existing islands
        to_add = []  # keep track of islands to merge
        for i, island in enumerate(self.islands):
            if self.is_adjacent(island, r, c):
                to_add.append(i)

        if to_add:
            return self.join_islands(to_add, r, c)
        else:
            self.islands.append({(r, c)})

    def is_adjacent(self, island, r, c) -> bool:
        """check if (r, c) is adjacent to island {i}"""
        for land in island:
            if abs(land[0] - r) + abs(land[1] - c) == 1:
                return True
        return False

    def join_islands(self, to_add, r, c):
        new = set()
        new.add((r, c))
        for i in to_add:
            new |= self.islands[i]
            self.islands[i] = None

        self.islands.append(new)
        self.islands = [i for i in self.islands if i is not None]


def test_is_same():
    r = RedPainting(3, 4)
    r.add_island(0, 0)
    r.add_island(0, 1)
    assert r.is_same(0, 0, 0, 1)

    r.add_island(2, 1)
    assert not r.is_same(0, 0, 2, 1)

    r.add_island(1, 1)
    assert r.is_same(0, 0, 2, 1)


def test_add_islands():
    r = RedPainting(3, 4)
    r.add_island(0, 0)
    r.add_island(0, 1)
    assert len(r.islands) == 1
    assert len(r.islands[0]) == 2

    r.add_island(2, 1)
    assert len(r.islands) == 2

    r.add_island(1, 1)
    assert len(r.islands) == 1


def test_join_islands():
    r = RedPainting(3, 4)
    r.islands = [{(0, 1), (0, 0)}, {(2, 1)}]
    r.join_islands([0, 1], 1, 1)
    assert len(r.islands) == 1
    assert len(r.islands[0]) == 4


def test_is_adjacent():
    r = RedPainting(3, 4)
    assert r.is_adjacent({(0, 0)}, 0, 1)


def test_add_one_island():
    r = RedPainting(3, 4)
    r.add_island(0, 0)
    assert len(r.islands) == 1


def main(H, W, Q, queries):
    ans = []
    grid = [[0] * W for _ in range(H)]
    for q in queries:
        if q[0] == 0:
            _, r, c = q
            grid[r][c] = 1
        if q[0] == 1:
            _, ra, ca, rb, cb = q
            if can_arrive(grid, ra, ca, rb, cb, H, W):
                ans.append("Yes")
                # print("Yes")
            else:
                ans.append("No")
                # print("No")
    return ans


from collections import deque


def can_arrive(grid, ra, ca, rb, cb, H, W):
    # wfs
    if not (grid[ra][ca] and grid[rb][cb]):
        return False
    visited = [[False] * W for _ in range(H)]
    Q = deque([(ra, ca)])
    while Q:
        r, c = Q.popleft()
        if not ((0 <= r < H) and (0 <= c < W)):
            continue
        if not grid[r][c]:
            continue
        if visited[r][c]:
            continue
        # do
        visited[r][c] = True
        if r == rb and c == cb:
            return True
        # add
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            Q.append((r + dx, c + dy))

    # couldn't reach
    return False


def test_can_arrive():
    grid = [[0, 0], [1, 1]]
    assert not can_arrive(grid, 0, 0, 1, 1, 2, 2)

    grid = [[1, 0], [1, 1]]
    assert can_arrive(grid, 0, 0, 1, 1, 2, 2)

    grid = [[1, 0], [0, 1]]
    assert not can_arrive(grid, 0, 0, 1, 1, 2, 2)
