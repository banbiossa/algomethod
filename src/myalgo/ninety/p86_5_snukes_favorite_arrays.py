def test_main():
    inputs = [
        """4 2
1 2 3 50
2 3 4 45
""",
        """8 2
2 3 6 1152886174205865983
1 2 8 1116611213275394047
"""
    ]
    answers = [13, 395781543]
    for text, answer in zip(inputs, answers):
        N, Q = map(int, text[0].split())
