def test_main():
    inputs = [
        """2
-1 2
1 1
""",
        """2
1 0
0 1
""",
        """5
2 5
2 5
-3 4
-4 -8
6 -2
""",
        """4
1000000000 1000000000
-1000000000 1000000000
-1000000000 -1000000000
1000000000 -1000000000
""",
    ]
    answers = [3, 2, 35, 8000000000]
    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        X = [None] * N
        Y = [None] * N
        for i in range(N):
            X[i], Y[i] = map(int, text.splitlines()[i + 1].split())
        assert main(N, X, Y) == answer


def median(X):
    X = sorted(X)
    N = len(X)
    if N % 2 == 1:
        return X[(N // 2)]
    else:
        return (X[(N // 2)] + X[(N // 2 - 1)]) / 2


def test_median():
    assert median([1, 1, 2, 3]) - 1.5 < 1e-5
    assert median([1, 2, 3]) - 2 < 1e-5


def main(N, X, Y):
    x_med = median(X)
    y_med = median(Y)
    x_part = f(X, x_med)
    y_part = f(Y, y_med)
    total = x_part + y_part
    return int(total)


def f(X, m):
    return sum([abs(x - m) for x in X])


def closest(X):
    left = min(X)
    right = max(X)
    res = f(X, left)
    at = left
    for i in range(left, right):
        fi = f(X, i)
        if fi < res:
            res = fi
            at = i
    return res, at


def _closest(X):
    left = min(X)
    right = max(X)
    while right - left > 1e-8:
        mid = (left + right) / 2
        if f(X, left) > f(X, right):
            left = mid
        else:
            right = mid
    return left


def test_closest():
    assert abs(closest([0, 1, -1])) < 1e-5
    assert abs(closest([1, 1, -1]) - 1) < 1e-5
