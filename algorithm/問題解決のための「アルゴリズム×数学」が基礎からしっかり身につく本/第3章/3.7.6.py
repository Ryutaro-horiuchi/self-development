N = int(input())
A = [0, *list(map(int, input().split()))]

dp = [0 for i in range(N+1)]
for i in range(N+1):
  if i == 0:
    dp[i] = 0
  else:
    dp[i] = max((A[i]+dp[i-2]), dp[i-1])

print(dp[-1])
