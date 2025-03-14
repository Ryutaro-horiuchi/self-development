n, r = map(int, input().split())
numerator = 1
denominator = 1
for i in range(r):
  numerator *= (n - i)
  denominator *= (r - i)

N=int(input())
ans = 1
for i in range(1, N+1):
  ans *= i

print(int(numerator / denominator))