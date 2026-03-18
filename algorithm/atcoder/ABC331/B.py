N,S,M,L = map(int, input().split())

ans = float("inf")
for i in range(N+12):
    for j in range(N+12):
        for k in range(N+12):
            if not (i*6 + j*8 + k*12) >= N:
                continue
            ans = min(ans, (i*S + j*M + k*L))
            
print(ans)
