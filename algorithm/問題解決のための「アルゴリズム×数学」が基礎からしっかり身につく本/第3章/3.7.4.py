N, S = map(int, input().split())
A = [0, *map(int, input().split())]

"""
カードiまでの間で合計がjとなる組み合わせがあるかどうか

・カードi-1の総和がjであり、カードiを選ばない
・カードi-1の総和がjーAiである時、カードiを選ぶ
"""

dp = [[False for j in range(S+1)] for _ in range(N+1)]

dp[0][0] = True

for i in range(1, N+1):
  for j in range(S+1):
    if dp[i-1][j]:
      dp[i][j] = True
    elif j >= A[i] and dp[i-1][j-A[i]]:
      dp[i][j] = True

print("Yes") if dp[N][S] else print("No")
