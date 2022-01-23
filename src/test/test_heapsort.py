from myalgo.heapsort import heapify, heapsort


def test_heapify():
    A = [1, 5, 2, 4]
    N = 4
    B = heapify(A, N)
    assert B == [5, 4, 2, 1]


def test_heapify_3():
    A = [1, 5, 2, 4, 7, 8]
    N = 4
    B = heapify(A, N)
    assert B == [5, 4, 2, 1, 7, 8]


def test_heapify2():
    N = 7
    A = [65, 35, 65, 87, 25, 25, 25]
    actual = heapify(A, N)
    expected = [87, 65, 65, 35, 25, 25, 25]
    assert actual == expected


def test_heapsort():
    N = 7
    M = 6
    A = [65, 35, 65, 87, 25, 25, 25]

    expected = [[65, 35, 65, 25, 25, 25, 87], [25, 25, 25, 35, 65, 65, 87]]
    actual = list(heapsort(A, N, M))

    assert actual[0] == expected[0]
    assert actual[1] == expected[1]


def test_heapsort2():
    N = 6
    M = 4
    A = [1, 4, 2, 8, 5, 7]

    expected = [[5, 4, 2, 1, 7, 8], [1, 2, 4, 5, 7, 8]]
    actual = heapsort(A, N, M)

    assert actual[0] == expected[0]
    assert actual[1] == expected[1]
