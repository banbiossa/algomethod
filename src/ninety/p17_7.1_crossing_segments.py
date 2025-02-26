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
]


def parse_qa(problem: QA) -> tuple:
    N, M = map(int, problem.question.split("\n")[0].split())
    segments = [list(map(int, x.split())) for x in problem.question.split("\n")[1:-1]]
    return N, M, segments, problem.answer


problem = problems[1]
N, M, segments, answer = parse_qa(problem)

logger.info(f"{N=}, {M=}, {segments=}, {answer=}")

# N<=1000, M<=1000 for q1, so we can do a M^2 solution
# we can look at each segments, if l1 < l2 < r1 < r2, then they cross

total = 0
for i in range(M):
    for j in range(M):
        l1, r1 = segments[i]
        l2, r2 = segments[j]
        if l1 < l2 < r1 < r2:
            total += 1

print(total)
