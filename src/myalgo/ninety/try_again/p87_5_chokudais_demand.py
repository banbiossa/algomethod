import heapq
import logging

from myalgo import profile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_main():
    logger.info("run test")
    inputs = [
        """3 4 2
0 3 -1
3 0 5
-1 5 0
        """,
        """3 10 2
0 -1 10
-1 0 1
10 1 0
        """,
        """13 777 77
0 425 886 764 736 -1 692 660 -1 316 424 490 423
425 0 -1 473 -1 311 -1 -1 903 941 386 521 486
886 -1 0 605 519 473 775 467 677 769 690 483 501
764 473 605 0 424 454 474 408 421 530 756 568 685
736 -1 519 424 0 -1 804 598 911 731 837 459 610
-1 311 473 454 -1 0 479 613 880 -1 393 875 334
692 -1 775 474 804 479 0 579 -1 -1 575 985 603
660 -1 467 408 598 613 579 0 456 378 887 -1 372
-1 903 677 421 911 880 -1 456 0 859 701 476 370
316 941 769 530 731 -1 -1 378 859 0 800 870 740
424 386 690 756 837 393 575 887 701 800 0 -1 304
490 521 483 568 459 875 985 -1 476 870 -1 0 716
423 486 501 685 610 334 603 372 370 740 304 716 0
        """,
    ]
    answers = [3, "Infinity", 42]
    for text, answer in zip(inputs, answers):
        N, P, K = map(int, text.splitlines()[0].split())
        A = []
        for i in range(N):
            a = list(map(int, text.splitlines()[i + 1].split()))
            A.append(a)
        assert main(N, P, K, A) == answer


"""
N 国: 2 <= N <= 40
P 以下で到達: 1 <= P <= 10**9

A[i][j] != -1 -> A[i][j]
A[i][j] == -1 => X

i -> j まで P 以下で到達可能な組はちょうど K 個存在する

X の選び方は何通りか

# 方針

1 <= X <= P+1 の範囲で、2分探索を行う
- X = P + 1 の場合は infinity

X を固定した際に、最短経路の数を出し、P 以下のものが K 以上存在するかいなかで分岐
- グラフの最短経路はダイクストラ？
"""


@profile
def main(N, P, K, A):
    logger.info(f"run main: {N=}, {P=}, {K=}, {A=}")

    # bisect x
    # input x


def input_x(A, x):
    return [[a if a != -1 else x for a in row] for row in A]


def test_input_x():
    A = [
        [-1, 3, 10],
        [3, 0, 1],
        [10, 1, 0],
    ]
    actual = input_x(A, None)

    expected = [
        [None, 3, 10],
        [3, 0, 1],
        [10, 1, 0],
    ]
    assert actual == expected
    assert A[0][0] == -1


def full(M):
    """行列Mに対してiからjにいく全通り"""
    return [dijkstra(M, i) for i in range(len(M))]


def dijkstra(M, i):
    """行列Mに対して頂点iから各頂点に行く最短距離"""
    n = len(M)
    heap = []  # maintains a list of items to go to
    done = {}  # the list of done parts
    heapq.heappush(heap, (0, i))  # add the initial point as distance 0

    while heap:
        dist, start = heapq.heappop(heap)  # pop the shortest of the existing
        if done.get(start) is None or done.get(start) > dist:
            done[start] = dist  # add that to done

        # for each of the edges from start, add to heap
        for j in range(n):
            if j in done:  # skip if already done
                continue
            new_dist = dist + M[start][j]
            heapq.heappush(heap, (new_dist, j))

    assert len(done) == n  # check that all points have a distance
    return [done[i] for i in range(n)]


def test_full():
    M = [
        [0, 3, 10],
        [3, 0, 1],
        [10, 1, 0],
    ]
    expected = [
        [0, 3, 4],
        [3, 0, 1],
        [4, 1, 0],
    ]
    actual = full(M)
    assert expected == actual


def test_dijkstra():
    M = [
        [0, 3, 10],
        [3, 0, 1],
        [10, 1, 0],
    ]
    dists = [
        [0, 3, 4],
        [3, 0, 1],
        [4, 1, 0],
    ]
    for i in range(3):
        actual = dijkstra(M, i)
        expected = dists[i]
        assert actual == expected


if __name__ == "__main__":
    test_main()
