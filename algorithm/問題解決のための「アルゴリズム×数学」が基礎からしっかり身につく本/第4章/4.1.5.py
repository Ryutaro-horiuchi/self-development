x = [0]
y = [0]
for i in range(4):
  _x, _y = map(int, input().split())
  x.append(_x)
  y.append(_y)

def cross(ax, ay, bx, by):
  return ax*by - bx*ay

ans1 = cross(x[2]-x[1], y[2]-y[1], x[3]-x[1], y[3]-y[1]) # AB, AC
ans2 = cross(x[2]-x[1], y[2]-y[1], x[4]-x[1], y[4]-y[1]) # AB, AD
ans3 = cross(x[4]-x[3], y[4]-y[3], x[1]-x[3], y[1]-y[3]) # CD, CA
ans4 = cross(x[4]-x[3], y[4]-y[3], x[2]-x[3], y[2]-y[3]) # CD, CB

if ans1 == 0 and ans2 == 0 and ans3 == 0 and ans4 == 0:
  A = (x[1], y[1])
  B = (x[2], y[2])
  C = (x[3], y[3])
  D = (x[4], y[4])
  if A > B:
    A,B = B,A
  if C > D:
    C,D = D,C
  
  if max(A, C) <= min(B,D):
    print('Yes')
  else:
    print('No')

else:
  IsAB = False
  IsCD = False

  if ans1 >= 0 and ans2 <=0: IsAB = True
  if ans1 <= 0 and ans2 >=0: IsAB = True
  if ans3 >= 0 and ans4 <=0: IsCD = True
  if ans3 <= 0 and ans4 >=0: IsCD = True

  if IsAB and IsCD:
    print('Yes')
  else:
    print('No')








