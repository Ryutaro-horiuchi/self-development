n, r = map(int, input().split())
numerator = 1
denominator = 1
for i in range(r):
  numerator *= (n - i)
  denominator *= (r - i)

print(int(numerator / denominator))