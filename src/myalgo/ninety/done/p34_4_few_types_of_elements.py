def test_main():
    inputs = [
        """5 1
1 2 3 4 5
""",
        """5 4
1 1 2 4 2
""",
        """10 2
1 2 3 4 4 3 2 1 2 3
""",
    ]
    answers = [1, 5, 4]

    for text, answer in zip(inputs, answers):
        N, K = map(int, text.splitlines()[0].split())
        a = list(map(int, text.splitlines()[1].split()))
        assert main(N, K, a) == answer


from collections import defaultdict


def main(N, K, a):
    # 尺取虫ぽくやってみる
    maxlen = 0
    start = 0
    count = 0
    distinct = defaultdict(int)

    for end in range(N):
        current = a[end]
        # keep track of all distinct
        distinct[current] += 1
        if distinct[current] == 1:
            count += 1

        # 切る
        while count > K:
            distinct[a[start]] -= 1
            if distinct[a[start]] == 0:
                count -= 1
            start += 1

        # 判定
        maxlen = max(maxlen, end - start + 1)
    return maxlen


if __name__ == "__main__":
    test_main()