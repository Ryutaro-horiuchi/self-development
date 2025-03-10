N=int(input())

root = N ** 0.5

ans = []
for i in range(2, N+1):
  while N % i == 0:
    N /= i
    ans.append(i)

if N >= 2:
  ans.append(N)

print(*ans)