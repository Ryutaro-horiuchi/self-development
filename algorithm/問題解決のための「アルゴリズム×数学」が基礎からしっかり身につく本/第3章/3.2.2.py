def GCD(a,b):
  """
  AとBの最大公約数を返す関数
  """
  while a >= 1 and b >= 1:
    if a > b:
      a = a % b
    else:
      b = b % a

  return max(a,b)

N=int(input())
A=list(map(int, input().split()))

gcd=GCD(A[0], A[1])
for i in A[2:]:
  gcd=GCD(gcd, i)

print(gcd)