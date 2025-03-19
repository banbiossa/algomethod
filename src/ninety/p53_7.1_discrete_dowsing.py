# インタラクティブになれるためのコード
# get an answer in 1500 steps

T = int(input())
for i in range(T):
    N = int(input())
    num = 0
    for j in range(N):
        # query
        print(f"? {j + 1}")
        num = max(num, int(input()))
    print(f"! {num}")
