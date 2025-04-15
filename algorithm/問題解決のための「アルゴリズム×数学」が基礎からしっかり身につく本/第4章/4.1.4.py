import math

A, B, H, M = map(int, input().split())

AngleH = 30.0 * H + 0.5 * M
AngleM = 6.0 * M

# 時針の座標
Hx = A * math.cos(AngleH * math.pi / 180.0)
Hy = A * math.sin(AngleH * math.pi / 180.0)

# 分針の座標
Mx = B * math.cos(AngleM * math.pi / 180.0)
My = B * math.sin(AngleM * math.pi / 180.0)

ans = math.sqrt((Hx - Mx)**2 + (Hy - My)**2)
print(ans)
