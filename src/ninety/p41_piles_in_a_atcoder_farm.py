"""
N
X1 Y1
...
XN YN
"""

problems = [
    (
        """3
1 4
6 1
5 8
""",
        17,
    ),
    (
        """10
72 7
54 25
97 48
37 47
34 54
4 16
62 1
59 22
99 73
34 75
""",
        4828,
    ),
    (
        """30
878317816 654163251
686185971 65193664
421988001 893301255
337790787 848308131
116633641 453711858
147679897 275450390
871549713 368160131
945135251 515070794
113677189 553747963
648722370 798825746
334960984 163211483
477414168 849868430
46724716 593116536
424597820 84043071
456749260 981436379
167906984 546584517
187306934 201207913
535850448 43428774
602081737 111568378
607467836 80430906
965538187 537789555
69199019 485172741
267885487 934316143
883812229 276272851
507976072 19708905
951100460 639017801
43859603 556279043
300658736 79240016
231304846 220059094
854667690 399502355
""",
        607281204170558988,
    ),
]


def parse_p(p):
    p = p.split("\n")
    N = int(p[0])
    xy = [list(map(int, x.split())) for x in p[1:-1]]

    return N, xy


problem = problems[2]
N, XY = parse_p(problem[0])

import logging  # noqa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


logger.debug(f"N: {N}, XY: {XY}")

# N = 3 の時は三角形
# 格子点の数を数える問題
# pick's theorm: i = S - 1/2*b + 1


def S(xs, ys):
    total = 0
    for i in range(len(xs)):
        # use -1 to loop around the end
        total += (xs[i - 1] - xs[i]) * (ys[i - 1] + ys[i])
    return abs(total) / 2


def S_times_2(xs, ys):
    total = 0
    for i in range(len(xs)):
        # use -1 to loop around the end
        total += (xs[i - 1] - xs[i]) * (ys[i - 1] + ys[i])
    return abs(total)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def gcds(xs, ys):
    total = 0
    for i in range(len(xs)):
        # use -1 to loop around the end
        total += gcd(
            abs(xs[i - 1] - xs[i]),
            abs(ys[i - 1] - ys[i]),
        )
        # actually gcd(foo) + 1 for edges
        # but we don't double count
    return total


if len(XY) == 3:
    i = S(*zip(*XY)) - gcds(*zip(*XY)) / 2 + 1

    # 周上も数える＋最初から何本かはある
    print(int(i + gcds(*zip(*XY)) - N))

# for the general case, we get the convex hull
# (and S, gcds, N from there)

from collections import deque  # noqa


# sort XY
XY.sort(key=lambda x: (x[0], x[1]))

logger.debug(f"sorted {XY=}")


def outer_product(p1, p2, p3):
    p1p2 = (p2[0] - p1[0], p2[1] - p1[1])
    p2p3 = (p3[0] - p2[0], p3[1] - p2[1])
    return p1p2[0] * p2p3[1] - p1p2[1] * p2p3[0]


# checker upper hull
upper_hull = [XY[0], XY[1]]
lower_hull = [XY[0], XY[1]]

for i in range(2, N):
    # upper hull should clockwise, outer product < 0
    while (
        len(upper_hull) >= 2
        and outer_product(upper_hull[-2], upper_hull[-1], XY[i]) > 0
    ):
        upper_hull.pop()

    while (
        len(lower_hull) >= 2
        and outer_product(lower_hull[-2], lower_hull[-1], XY[i]) < 0
    ):
        lower_hull.pop()

    upper_hull.append(XY[i])
    lower_hull.append(XY[i])


logger.debug(f"{upper_hull=}")
logger.debug(f"{lower_hull=}")

full_hull = upper_hull + lower_hull[1:-1][::-1]
logger.debug(f"{full_hull=}")

# i = S(*zip(*full_hull)) - gcds(*zip(*full_hull)) / 2 + 1
# ans = i + gcds(*zip(*full_hull)) - N
# logger.info(f"S = {S(*zip(*full_hull))}")
# logger.info(f"gcds = {gcds(*zip(*full_hull))}")
# logger.info(f"i = {i}")
# print(int(ans))

# let's try not going to floats, so use 2S and 2gcds, //2 at the end
ans_times_2 = S_times_2(*zip(*full_hull)) + gcds(*zip(*full_hull)) + 2 - 2 * N
logger.info(f"{ans_times_2=}")
print(ans_times_2 // 2)
