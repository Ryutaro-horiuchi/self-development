H, W = map(int, input().split())
a = (H+1) // 2
b = (W+1) // 2

ans = a*b
if min(H, W) == 1:
    print(max(H, W))
else:
    print(ans)