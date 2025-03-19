T = int(input())
for _ in range(T):
    n = int(input())
    l, m1, m2, r = 0, 610, 987, 1597
    a = [-i for i in range(1598)]
    a[0] = 0

    while True:
        if m1 <= n and a[m1] < 0:
            print("?", m1)
            a[m1] = int(input())
        if m2 <= n and a[m2] < 0:
            print("?", m2)
            a[m2] = int(input())
        if r - l > 3:
            if a[m1] > a[m2]:
                m1, m2, r = l + m2 - m1, m1, m2
            else:
                l, m1, m2 = m1, m2, r + m1 - m2
        else:
            print("!", max(a[l : r + 1]))
            break
