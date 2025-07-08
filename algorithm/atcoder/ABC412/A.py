from functools import reduce

N, M = map(int, input().split())
n = reduce(lambda x,y: x+y, list(map(int, input().split())))
if M >= n:
  print("Yes")
else:
  print("No")
