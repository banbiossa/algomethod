problems = [
    (999, 434, 2),
    (255, 15, 2),
    (9999999999, 1, 0),
]

N, B, ans = problems[0]

# if you sort x, the f(x) is the same (247 and 742)
# so for S, if f(S) + B = T and T is a permutation of S, then S is a valid answer
# the total number of S is 20C10, so it can be done in time

# say we get a S like ["2", "4", "7"]

from functools import reduce


# compute f(S)
def f(S):
    return reduce(lambda x, y: x * y, S)


def check_s(S, B):
    T = B + f(S)
    if T > N:
        return False
    return sorted([int(a) for a in str(T)]) == S


# so we need to generate all possible S
def dfs(s: str, nex: int, max_len: int):
    if s:
        yield s
    if len(s) == max_len:
        return
    for i in range(nex, 10):
        yield from dfs(s + str(i), i, max_len)


total = 0
if B <= N and "0" in str(B):
    total += 1

for i in dfs("", 1, 11):
    S = [int(a) for a in i]
    if check_s(S, B):
        total += 1
print(total)
