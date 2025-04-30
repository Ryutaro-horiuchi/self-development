N,M = map(int, input().split())
A = [None] * M
B = [None] * M
for i in range(M):
  a,b = map(int, input().split())
  A[i], B[i] = a,b

G = [list() for i in range(N+1)]
for i in range(M):
  G[A[i]].append(B[i])
  G[B[i]].append(A[i])

ans = 0
for idx, g in enumerate(G):
  count = 0
  while count <= 1:
    for i in g:
      if i < idx:
        count+= 1
    break

  if count == 1:
    ans+= 1

print(ans)





  
