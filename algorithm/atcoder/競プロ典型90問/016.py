N = int(input())
A,B,C = map(int, input().split())

P = 10000
ans = P
for a in range(P):
    for b in range(P):
        AB = A*a + B*b
        if N < AB or (N - AB) % C != 0:
            continue

        c = (N - AB) // C
        ans = min(ans, a+b+c)
print(ans)