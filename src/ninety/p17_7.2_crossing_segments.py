import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


@dataclass
class QA:
    question: str
    answer: int


problems = [
    QA(
        question="""6 3
2 5
1 4
1 3
""",
        answer=2,
    ),
    QA(
        question="""250 10
13 218
17 99
24 180
53 115
96 97
111 158
124 164
135 227
158 177
204 224
""",
        answer=10,
    ),
    QA(
        question="""100 10
1 2
1 3
1 4
1 5
1 6
1 7
1 8
1 9
1 10
1 11
""",
        answer=0,
    ),
    QA(
        question="""1000 40
12 43
23 59
32 118
44 751
68 136
70 168
85 328
88 809
92 981
95 540
98 772
98 903
125 896
173 737
199 325
212 369
227 587
230 374
287 442
306 926
314 858
316 371
318 493
337 506
384 887
387 493
394 457
404 652
414 527
422 920
441 730
445 620
468 602
482 676
568 857
587 966
653 757
710 928
764 927
778 916
""",
        answer=229,
    ),
]


def parse_qa(problem: QA) -> tuple:
    N, M = map(int, problem.question.split("\n")[0].split())
    segments = [list(map(int, x.split())) for x in problem.question.split("\n")[1:-1]]
    return N, M, segments, problem.answer


problem = problems[3]
N, M, segments, answer = parse_qa(problem)

# make the segments 0-indexed
segments = [[x - 1, y - 1] for x, y in segments]

logger.info(f"{N=}, {M=}, {segments=}, {answer=}")

# second  step is N<=1000, M<=100,000
# so we can't do a M^2 solution
# N is relatively small so must be something there
# probablly NM <= 10**9 so sounds like DP?

# we count the not-happens
# for [Ls, Rs] and [Lt, Rt]
# 1. same i -> sum(cnt_i * (cnt_i - 1) // 2)
# 2. Rs < Lt
# 3. Ls Lt Rt Rs

# 1. same i
# for each i, count the number of segments
count = [0] * N
for i in range(M):
    l, r = segments[i]
    count[l] += 1
    count[r] += 1

total_1 = sum([x * (x - 1) // 2 for x in count])
logger.info(f"{count=}, {total_1=}")

# 2. Rs < Lt
# count where Rs <= i, by counting Rs==i and adding up
count_r = [0] * N
for i in range(M):
    _, r = segments[i]
    count_r[r] += 1

count_up_r = [0] * (N + 1)
for i in range(N):
    count_up_r[i + 1] = count_up_r[i] + count_r[i]
logger.info(f"{count_r=}, {count_up_r=}")

total_2 = 0
for i in range(M):
    l, _ = segments[i]
    total_2 += count_up_r[l]

logger.info(f"{total_2=}")

# 3. Ls Lt Rt Rs
# add from the smaller Rs
# if Ls < Lt than add (this means finding Lt=i)

# sort the segments by the right end
# this should be O(MlogM) so ok, smaller than O(NM)
# log(10**5) ~= 17 << 1000
logger.info(f"{sorted(segments)=}")
segments.sort(key=lambda x: (x[1], x[0]))

logger.info(f"{segments=}")
count_l = [0] * N
total_3 = 0
for i in range(M):
    l, r = segments[i]
    for j in range(l + 1, r):
        total_3 += count_l[j]
    count_l[l] += 1

logger.info(f"{total_3=}")

total = total_1 + total_2 + total_3
res = M * (M - 1) // 2 - total
logger.info(f"{total=}, {M*(M-1)//2=}, {res=}")
logger.info(f"{res=}, {answer=}")
print(res)
