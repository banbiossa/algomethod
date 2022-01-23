class UnionFind:
    def __init__(self, n, w):
        self.n = n
        self.par = [-1] * n
        self.w = w  # weights of individual
        self.size = w.copy()  # total weight

    def root(self, x):
        if self.par[x] == -1:
            return x
        self.par[x] = self.root(self.par[x])
        return self.par[x]

    def union(self, x, y):
        rx, ry = self.root(x), self.root(y)
        if rx == ry:
            return False

        # make y the smaller parent
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx

        self.par[rx] = ry
        self.size[ry] += self.size[rx]
        return True

    def weight(self, x):
        return self.size[self.root(x)]
