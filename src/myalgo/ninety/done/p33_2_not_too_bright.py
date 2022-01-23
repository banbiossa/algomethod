def test_main():
    inputs = [[2, 3], [3, 4], [3, 6]]
    answers = [2, 4, 6]
    for text, answer in zip(inputs, answers):
        H, W = text
        assert main(H, W) == answer


def main(H, W):
    if H == 1 or W == 1:
        return H * W
    return ((H + 1) // 2) * ((W + 1) // 2)
