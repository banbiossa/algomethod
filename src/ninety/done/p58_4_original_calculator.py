def test_main():
    inputs = ["5 3", "0 100", "99999 1000000000000000000"]
    answers = [13, 0, 84563]

    for text, answer in zip(inputs, answers):
        N, K = map(int, text.split())
        assert main(N, K) == answer


def main(N, K):
    BIG = 10 ** 5
    ans = [N]

    end_loop = True
    x = N
    for i in range(K):
        y = sum(map(int, [a for a in str(x)]))
        z = (x + y) % BIG
        x = z
        if x in ans:
            end_loop = False
            break
        ans.append(x)
    if end_loop:
        return x

    loop_start = ans.index(x)
    loop = ans[loop_start:]

    index = (K - loop_start) % len(loop)
    v = loop[index]
    return v
