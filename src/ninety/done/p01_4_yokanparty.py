def make(x, A):
    """長さxを作れる個数"""
    count = 0
    tmp = 0
    for a in A:
        tmp += a
        if tmp >= x:
            tmp = 0
            count += 1
    return count


def can_make(x, n, A):
    """xをnこ作れるか"""
    return make(x, A) >= n


def lengths(A, L, N):
    """切れ目の位置からようかんの長さを割り出す"""
    B = [0] + A + [L]
    return [B[i + 1] - B[i] for i in range(N + 1)]


def binary_search(N, L, K, A):
    B = lengths(A, L, N)
    left = 0
    right = L

    while left != right:
        mid = (left + right + 1) // 2
        if can_make(mid, K + 1, B):
            left = mid
        else:
            right = mid - 1

    return left


def test_binary_search():
    texts = [
        """3 34
        1
        8 13 26""",
        """7 45
        2
        7 11 16 20 28 34 38""",
        """3 100
        1
        28 54 81""",
        """3 100
        2
        28 54 81""",
        """20 1000
        4
        51 69 102 127 233 295 350 388 417 466 469 523 553 587 720 739 801 855 926 954""",
    ]
    answers = [13, 12, 46, 26, 170]
    for text, answer in zip(texts, answers):
        N, L = map(int, text.splitlines()[0].split())
        K = int(text.splitlines()[1])
        A = list(map(int, text.splitlines()[2].split()))
        assert binary_search(N, L, K, A) == answer


def test_lengths():
    assert lengths([1, 2], 3, 2) == [1, 1, 1]
    assert lengths([2, 4, 6], 9, 3) == [2, 2, 2, 3]


def test_make():
    assert make(3, [1, 2, 3]) == 2
    assert make(4, [1, 1, 1]) == 0
