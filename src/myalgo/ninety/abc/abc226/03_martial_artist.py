def test_main():
    inputs = [
        """3
3 0
5 1 1
7 1 1
""",
        """5
1000000000 0
1000000000 0
1000000000 0
1000000000 0
1000000000 4 1 2 3 4
""",
    ]
    answers = [10, 5000000000]

    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])
        waza = {}
        for i in range(N):
            row = list(map(int, text.splitlines()[i + 1].split()))
            t = row[0]
            k = row[1]
            a = row[2:]
            waza[(i + 1)] = (t, a)
        assert main(N, waza) == answer


from collections import deque


def main(N, waza):
    learned = set()
    total = 0
    Q = deque([N])
    while Q:
        w = Q.popleft()
        t, need = waza[w]

        if w in learned:
            continue

        total += t
        learned.add(w)
        for a in need:
            Q.append(a)
    return total
