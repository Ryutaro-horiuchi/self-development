T=int(input())
N=int(input())
B = [0 for i in range(T)]

for i in range(N):
  start,end = map(int, input().split())
  B[start] += 1
  B[end] -= 1

ans = 0
for i in B:
  ans += i
  print(ans) 
