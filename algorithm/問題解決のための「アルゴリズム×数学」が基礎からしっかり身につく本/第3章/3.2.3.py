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


def LCM(a,b):
  """
  AとBの最小公倍数を返す関数
  """
  return int(a / GCD(a,b)) * b


N=int(input())
A=list(map(int, input().split()))

lcm=LCM(A[0], A[1])
for i in A[2:]:
  lcm=LCM(lcm, i)

print(lcm)