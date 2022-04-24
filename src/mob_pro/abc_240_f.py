def main(N):
    total = 0
    for i in range(1, N):
        if i * i > N:
            break
        length = (N // i)
        total += 2 * (length - i+1) - 1
    return total


def test_main():
    assert main(3) == 5
    assert main(10000000000) == 231802823220


