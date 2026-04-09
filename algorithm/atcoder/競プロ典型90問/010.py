N = int(input())
C = {1: [0], 2: [0]}

for _ in range(N):
    c, p =  map(int, input().split())
    C[c].append(p+C[c][-1])

    another = 1 if c - 1 == 1 else 2
    C[another].append(C[another][-1])

Q = int(input())

for _ in range(Q):
    l, r = map(int, input().split())
    print(C[1][r] - C[1][l-1], end=" ")
    print(C[2][r] - C[2][l-1])