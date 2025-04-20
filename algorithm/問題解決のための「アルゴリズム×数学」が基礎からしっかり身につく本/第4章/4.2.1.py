N=int(input())
A=[0, *list(map(int, input().split()))]
M=int(input())

B = []
for _  in range(M):
  B.append(int(input()))

S = [0,0]
for i in range(2, N+1):
  s = S[i-1] + A[i-1]
  S.append(s)

ans = 0
for i in range(M-1):
  if (B[i] < B[i+1]):
    ans += S[B[i+1]] - S[B[i]]
  else:
    ans += S[B[i]] - S[B[i+1]]
print(ans)