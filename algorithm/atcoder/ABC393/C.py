N, M = map(int, input().split())
G = [[] for _ in range(N+1)]

cnt = 0
for _ in range(M):
    u, v = map(int, input().split())
    if u == v or (v in G[u] and u in G[v]):
        cnt += 1
        continue

    G[u].append(v)
    G[v].append(u)
print(cnt)