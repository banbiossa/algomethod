def test_main():
    inputs = [
        """4
2 1 2
2 1 1
2 2 1
2 1 2
""",
        """5
1 1
1 1
1 2
2 1 1
3 1 1 1
""",
        """1
1 1
""",
    ]
    answers = [3, 4, 1]
    for text, answer in zip(inputs, answers):
        N = int(text.splitlines()[0])

        a = set()
        for i in range(N):
            a.add(tuple(map(int, text.splitlines()[i + 1].split())))

        assert len(a) == answer


def main():
    a = set()
    a.add((3, 2, 1))
    a.add((3, 2, 1))
    assert len(a) == 1
