# TLE

from itertools import permutations

N, M = map(int, input().split())

base = [[False] * N for _ in range(N)]

for i in range(M):
  a, b = map(int, input().split())
  a -= 1
  b -= 1
  if a > b:
    a, b = b, a
  base[a][b] = True

ans = float('inf')

for perm in permutations(range(N)):
  g = [[False] * N for _ in range(N)]
  for i in range(N):
    a, b = perm[i], perm[(i+1) % N]
    if a > b:
      a, b = b, a
    g[a][b] = True

  cnt1 = 0
  for a in range(N):
    for b in range(N):
      if base[a][b] != g[a][b]:
        cnt1 += 1

  ans = min(ans, cnt1)

  for d in range(3, N-2+1): # 連結成分は2つ。取れる頂点数は3から最大で6まで
    h = [[False] * N for _ in range(N)]

    # 最初のサイクル
    for i in range(d):
      a, b = perm[i], perm[(i+1) % d]
      if a > b:
        a, b = b, a
      h[a][b] = True

    for i in range(N-d):
      a, b = perm[i+d], perm[(i+1) % (N-d) + d]
      if a > b:
        a, b = b, a
      h[a][b] = True

    cnt2 = 0
    for a in range(N):
      for b in range(N):
        if base[a][b] != h[a][b]:
          cnt2 += 1

    ans = min(ans, cnt2)

print(ans)