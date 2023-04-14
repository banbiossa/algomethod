class CombiModInv:
    def __init__(self, n, mod):
        self.n = n
        self.mod = mod
        #
        fact = [1] * (n + 1)  # fact[n] = (n! % mod)
        for i in range(1, n + 1):
            fact[i] = (fact[i - 1] * i) % mod
        self.fact = fact

    #
    def _inv(self, x):
        return pow(x, self.mod - 2, self.mod)

    #
    def nCr(self, n, r):
        # 組み合わせ(combinations)
        if (r < 0) or (n < r):
            return 0
        return self.fact[n] * self._inv(self.fact[r] * self.fact[n - r]) % self.mod

    #
    def nPr(self, n, r):
        # 順列(permutations)
        if (r < 0) or (n < r):
            return 0
        return self.fact[n] * self._inv(self.fact[n - r]) % self.mod

    #
    def nHr(self, n, r):
        # 重複組み合わせ
        if n == r == 0:
            return 1
        return self.nCr(n + r - 1, r)


#
# 使い方
#


def main(N, k):
    combimodinv = CombiModInv(N, P)
    ans = 0
    for a in range(1, N + 1):
        num = combimodinv.nCr(N - (k - 1) * (a - 1), a)
        if num == 0:
            break
        ans = (ans + num) % P
    return ans


def everything(N, P):

    res = []
    for k in range(1, N + 1):
        res.append(main(N, k))
    return res


if __name__ == "__main__":
    N = int(input())
    P = 10**9 + 7

    res = everything(N, P)

    for r in res:
        print(r)
