def test_main():
    inputs = [
        """8 5
6 17 2 4 17 19 1 7
2 0 0
1 7 2
1 2 6
1 4 5
3 4 0
""",
        """9 6
16 7 10 2 9 18 15 20 5
2 0 0
1 1 4
2 0 0
1 8 5
2 0 0
3 6 0
""",
        """11 18
23 92 85 34 21 63 12 9 81 44 96
3 10 0
3 5 0
1 3 4
2 0 0
1 4 11
3 11 0
1 3 5
2 0 0
2 0 0
3 9 0
2 0 0
3 6 0
3 10 0
1 6 11
2 0 0
3 10 0
3 4 0
3 5 0
""",
    ]
    answers = [
        "4",
        "18",
        """44
21
34
63
85
63
21
34
96
""",
    ]
    for text, answer in zip(inputs, answers):
        N, Q = map(int, text.splitlines()[0].split())
        A = list(map(int, text.splitlines()[1].split()))
        queries = []
        for i in range(Q):
            queries.append(
                list(map(lambda x: int(x) - 1, text.splitlines()[i + 2].split()))
            )
        assert main(N, Q, A, queries) == list(map(int, answer.split()))
        assert ac(N, Q, A, queries) == list(map(int, answer.split()))


def main(N, Q, A, queries):
    A = A.copy()
    ans = []
    for (t, x, y) in queries:
        if t == 0:
            A[x], A[y] = A[y], A[x]
        if t == 1:
            A = [A[-1]] + A[:-1]
        if t == 2:
            ans.append(A[x])
    return ans


def ac(N, Q, A, queries):
    A = A.copy()
    ans = []
    shift = 0
    for (t, x, y) in queries:
        if t == 0:
            xn = (x - shift) % N
            yn = (y - shift) % N
            A[xn], A[yn] = A[yn], A[xn]
        if t == 1:
            shift += 1
        if t == 2:
            xn = (x - shift) % N
            ans.append(A[xn])
    return ans
