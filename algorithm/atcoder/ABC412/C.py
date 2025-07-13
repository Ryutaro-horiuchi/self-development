def func(S, start, cnt):
  try:
    ans = max([value for value in S if value <= start*2 and value > start])
  except ValueError:
    return -1

  last = S[-1] 
  if ans >= last:
    return cnt

  return func(S, ans, cnt+1)

T=int(input())
for _ in range(T):
  N = int(input())
  S = list(map(int, input().split()))

  cnt = 2
  if 2 * S[0] >= S[-1]:
    print(cnt)
    continue

  ans = func(S, S[0], cnt)
  print(ans)