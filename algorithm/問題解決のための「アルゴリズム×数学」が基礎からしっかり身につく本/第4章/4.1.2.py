from math import sqrt

N=int(input())
points = [list(map(int, input().split())) for _ in range(N)]

ans = 10**6

for i in range(N):
  for j in range(N):
    if i == j:
      continue

    a = points[i]
    b = points[j]
    x = b[0] - a[0]
    y = b[1] - a[1]
    ans = min(sqrt(x**2 + y**2), ans)

print(ans)
