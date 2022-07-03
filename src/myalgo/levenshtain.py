S = input()
T = input()

sl = len(S)
tl = len(T)

dp = [[None] * tl for _ in range(sl)]

# I think we need to put in
# a: append
# r: replace
# d: delete
#
# the markov chain is
# if same
#   i, j -> r
#   else -> a
# if not same
#   a -> d
#   r -> r
#   d -> d

for i in range(sl):
    for j in range(tl):
        # init
        if i == 0 and j == 0:
            if S[i] == T[j]:
                dp[i][j] = ""
            else:
                dp[i][j] = "a"
            break

        # routes
        routes = []
        if i > 0 and j > 0 and dp[i - 1][j - 1] is not None:
            routes.append(("ij", dp[i - 1][j - 1]))
        if i > 0 and dp[i - 1][j] is not None:
            routes.append(("i", dp[i - 1][j]))
        if j > 0 and dp[i][j - 1] is not None:
            routes.append(("j", dp[i][j - 1]))

        # sort by length and take first
        routes.sort(key=lambda x: (len(x[1]), -len(x[0])))
        key, route = routes[0]

        # same route
        if S[i] == T[j]:
            # a -> d
            # r -> r
            # d -> d
            if route[-1] == "a":
                dp[i][j] = route[:-1] + "d"
            else:
                dp[i][j] = route + ""
            if i < sl - 1:
                break

        # different route
        else:
            # i, j -> r
            # else -> a
            if key == "ij":
                dp[i][j] = route + "r"
            if key == "j":
                dp[i][j] = route + "a"
            if key == "i":
                dp[i][j] = route + "d"

print(len(dp[-1][-1]))
for row in dp:
    # continue
    print(row)
