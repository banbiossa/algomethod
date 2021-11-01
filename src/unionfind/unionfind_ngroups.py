class UnionFind:
    def __init__(self, n):
        self.n = n  # num groups
        self.par = [-1] * n
        self.h = [0] * n  # height

    def root(self, x):
        if self.par[x] == -1:
            return x
        self.par[x] = self.root(self.par[x])
        return self.par[x]

    def join(self, x, y):
        rx = self.root(x)
        ry = self.root(y)
        if rx == ry:
            return False
        # force rx >= ry (ry is parent)
        if self.h[rx] < self.h[ry]:
            rx, ry = ry, rx
        self.par[rx] = ry
        if self.h[rx] == self.h[ry]:
            self.h[ry] += 1
        # decrement if join happens
        self.n -= 1
        return True
