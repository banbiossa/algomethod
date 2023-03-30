"""
- N個のP、P[i] = (X[i], Y[i])の点が与えられる
- Pi, pj, pkの3点のなす角を最大化する
"""


"""
方針
- 1回三点のなす角を求める. ググったら出てきそう.
    - 出てきた

- アホにやるとi,j,k の順列なのでN^3
    - N が2000なので 8*10**9は普通間に合わなさそう？
    - が、他には思いつかないのでやるしかない
    - 手元テストが通れば一旦合格としよう

- 答えを見たので、原点マイナスからの偏角ソートをする
"""

import math
from bisect import bisect_left


def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dotproduct(v, v))


def angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


def test_angle():
    assert angle((1, 0), (0, 1)) == math.pi / 2
    assert angle((1, 0), (1, 0)) == 0
    assert angle((1, 0), (-1, 0)) == math.pi
    assert angle((1, 0), (0, -1)) == math.pi * 1 / 2


def main(N, P):
    # 原点を定める（ループする）
    # 原点を引く
    # 偏角を求める（arctan2)
    # 偏角をソートする
    # 180に最も近いものを2部探索で探す
    closest_angle = 0

    # 原点を定める（ループする）
    for i in range(N):
        # 原点を引くが、自分自身は除く
        P_ = [(x - P[i][0], y - P[i][1]) for j, (x, y) in enumerate(P) if i != j]
        # 偏角を求める（arctan2)
        angles = [argument(x, y) for x, y in P_]
        # 偏角をソートする
        angles.sort()
        # 180に最も近いものを2部探索で探す
        for ang in angles:
            target = (ang + 180) % 360
            pos = bisect_left(angles, target)
            NN = N - 1  # for index error, mod を取ると先頭になって答えはおかしいが、範囲外なので構わない
            n1 = (angles[pos % NN] - ang) % 360
            n2 = (angles[(pos - 1) % NN] - ang) % 360
            closest_angle = max(closest_angle, min(n1, 360 - n1), min(n2, 360 - n2))

    return closest_angle


def find_closest(ang, angles):
    # this needs to be mod 360
    angles = [(a - ang) % 360 for a in angles]
    # find closest to 180
    left = 0
    right = len(angles) - 1
    while right - left > 1:
        mid = (left + right) // 2
        if angles[mid] > 180:
            right = mid
        else:
            left = mid
    if abs(angles[left] - 180) < abs(angles[right] - 180):
        ans = angles[left]
        return ans
    else:
        ans = angles[right]
        return ans


def argument(x, y):
    return math.degrees(math.atan2(y, x)) % 360


def main_(N, P):
    """
    P: list of tuple of int
    """
    max_angle = 0
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if P[i] == P[j] or P[j] == P[k] or P[k] == P[i]:
                    continue
                ang = point_to_angle(P[i], P[j], P[k])
                max_angle = max(ang, max_angle)

    return max_angle


def point_to_angle(Pi, Pj, Pk):
    """
    Pi, Pj, Pkのなす角を求める
    """
    v_ji = (Pi[0] - Pj[0], Pi[1] - Pj[1])
    v_jk = (Pk[0] - Pj[0], Pk[1] - Pj[1])
    ang = angle(v_ji, v_jk)
    return radian_to_angle(ang)


def radian_to_angle(rad):
    return rad * 180 / math.pi


def test_main():
    inputs = [
        """3
0 0
0 10
10 10
""",
        """5
8 6
9 1
2 0
1 0
0 1
""",
        """10
0 0
1 7
2 6
2 8
3 5
5 5
6 7
7 1
7 9
8 8
""",
        """40
298750376 229032640
602876667 944779015
909539868 533609371
231368330 445484152
408704870 850216874
349286798 30417810
807260002 554049450
40706045 380488344
749325840 801881841
459457853 66691229
5235900 8100458
46697277 997429858
827651689 790051948
981897272 271364774
536232393 997361572
449659237 602191750
294800444 346669663
792837293 277667068
997282249 468293808
444906878 702693341
894286137 845317003
27053625 926547765
739689211 447395911
902031510 326127348
582956343 842918193
235655766 844300842
438389323 406413067
862896425 464876303
68833418 76340212
911399808 745744264
551223563 854507876
196296968 52144186
431165823 275217640
424495332 847375861
337078801 83054466
648322745 694789156
301518763 319851750
432518459 772897937
630628124 581390864
313132255 350770227
""",
    ]
    answers = [
        90,
        171.869897645844,
        180,
        179.9834340684232,
    ]
    for the_input, expected in zip(inputs, answers):
        N = int(the_input.splitlines()[0])
        P = []
        for i in range(N):
            x, y = map(int, the_input.splitlines()[i + 1].split())
            P.append((x, y))
        actual = main(N, P)
        assert math.isclose(actual, expected, rel_tol=1e-5)


if __name__ == "__main__":
    N = int(input())
    P = []

    for i in range(N):
        x, y = map(int, input().split())
        P.append((x, y))
    print(main(N, P))
