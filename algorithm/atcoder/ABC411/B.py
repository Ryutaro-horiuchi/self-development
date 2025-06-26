def func(d):
  ans = 0
  for i in d:
    ans += i
    print(ans, end=' ')
  print('')
  
N = int(input())
D = list(map(int, input().split()))
for i in range(N):
  func(D[i:N])