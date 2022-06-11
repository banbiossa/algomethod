def test_main():
    inputs = ["3.456", "99.500", "0.000"]
    answers = [3, 100, 0]
    for text, answer in zip(inputs, answers):
        x = float(text)
        assert main(x) == answer


def main(n):
    return round(n)
