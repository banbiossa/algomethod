import logging

from myalgo import profile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

BIG = 1000000007


def test_main():
    inputs = [
        """4 2
1 2 3 50
2 3 4 45
""",
        """8 2
2 3 6 1152886174205865983
1 2 8 1116611213275394047
""",
    ]
    answers = [13, 395781543]
    for text, answer in zip(inputs, answers):
        N, Q = map(int, text.split("\n")[0].split())
        qs = []
        for i in range(Q):
            x, y, z, w = map(lambda t: int(t) - 1, text.split("\n")[i + 1].split())
            w += 1
            qs.append((x, y, z, w))

        assert main(N, Q, qs) == answer
        print("done")


"""
どうやって全探索するか

A: N桁の数列,それぞれ60桁のbinary

i: [0, Q]  query
j: [0, N]  与えられる数

k: w, A[j] の桁

x[i], y[i], z[i]: j のうちのどれか
w[i]: OR が満たすべき整数
bin_w_i: w[i] の binary, これの k桁目を比較する

60 桁のリスト= []

全ての k[0:60] に対して for k in range(60)
    k 桁目の候補数 = 0

    k 桁目のこの組み合わせが  for mask in range(2**N)
        全ての query に関して  # for i in range(Q):
            条件を満たす場合 mask[x] | mask[y] | mask[z] == bin_w_i[k]
                continue
            else:
                break

        k 桁目の候補に加算する

    60桁のリストに append

60桁のリストを全て掛け算して BIG で割る
"""


@profile
def main(N, Q, qs):
    ans = 1
    for k in range(60):
        count = 1 << N  # decrement していく
        for mask in range(1 << N):

            for i in range(Q):
                x, y, z, w = qs[i]

                if (mask >> x & 1) | (mask >> y & 1) | (mask >> z & 1) != (w >> k & 1):
                    count -= 1
                    break  # did not meet criteria

        # result for k
        ans *= count
        ans %= BIG

    return ans


if __name__ == "__main__":
    test_main()
