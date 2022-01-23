from myalgo.ninety.p81_5_friendly_group import main

def test_main():
    inputs = [
        """3 4
1 1
2 5
7 4
""",
        """2 123
4 5
678 901
""",
        """7 10
20 20
20 20
20 30
20 40
30 20
30 30
40 20
""",
    ]
    answers = [2, 1, 5]

    for text, answer in zip(inputs, answers):
        N, K = map(int, text.splitlines()[0].split())
        query = []
        for i in range(N):
            a, b = map(int, text.splitlines()[i + 1].split())
            query.append((a, b))

        assert main(N, K, query) == answer