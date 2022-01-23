def swap(A, k, n):
    while 2 * k + 1 < n:
        l, r = 2 * k + 1, 2 * k + 2
        if r < n and A[r] > A[k] and A[r] > A[l]:
            A[k], A[r] = A[r], A[k]
        elif A[l] > A[k]:
            A[k], A[l] = A[l], A[k]
            k = l
        else:
            return A
    return A


def hsort(A, n, m):
    for k in range(n // 2 - 1, -1, -1):
        A = swap(A, k, n)
    for i in range(n - 1, 0, -1):
        A[0], A[i] = A[i], A[0]
        A = swap(A, 0, i)
        if i == m:
            print(*A)
    return A




def heapify(A, N):
    for x in range(N // 2 - 1, -1, -1):
        k = x
        while True:
            # 子ノードの有無
            if 2 * k + 1 >= N:
                break
            # get the max and index
            m = A[k]
            i = k
            if A[2 * k + 1] > A[k]:
                m = A[2 * k + 1]
                i = 2 * k + 1
            if 2 * k + 2 < N and A[2 * k + 2] > m:
                m = A[2 * k + 2]
                i = 2 * k + 2
            # swap
            if i == k:
                break
            if i == 2 * k + 1:
                A[k], A[2 * k + 1] = A[2 * k + 1], A[k]
                k = 2 * k + 1
            if i == 2 * k + 2:
                A[k], A[2 * k + 2] = A[2 * k + 2], A[k]
                k = 2 * k + 2
    return A


def heapsort(A, N, M):
    A = heapify(A, N)
    print(A)
    result = []
    for i in range(N - 1, 0, -1):
        A[0], A[i] = A[i], A[0]
        print(A)
        A = heapify(A, i)
        print(A)
        if i == M:
            result.append(A.copy())
            print(*A)
    result.append(A)
    return result

if __name__ == "__main__":
    n, m = map(int, input().split())
    A = list(map(int, input().split()))
    A = hsort(A, n, m)
    print(*A)
