import math

x1, y1, r1 = map(int, input().split())
x2, y2, r2 = map(int, input().split())
distance = math.sqrt((x2 - x1)**2 + (y2 - y1) **2)
pattern2 = abs(r1-r2)
pattern4 = r1+r2

ans = 0
if distance <= pattern2:
  if distance == pattern2:
    ans = 2
  else:
    ans = 1
elif distance < pattern4:
  ans = 3
elif distance == pattern4:
  ans = 4
else:
  ans = 5

print(ans)