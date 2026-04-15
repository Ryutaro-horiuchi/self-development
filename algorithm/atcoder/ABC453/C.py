n = int(input())
L = list(map(int, input().split()))

t = 0.5
ans = 0

def rec(idx, cnt, t):
    global ans
    if idx > n-1:
        ans = max(ans, cnt)
        return

    value = L[idx]
    plus_cnt = cnt
    if t < 0 and (t + value > 0):
        plus_cnt += 1
    rec(idx+1, plus_cnt, t + value)

    minus_cnt = cnt
    if t > 0 and (t - value < 0):
        minus_cnt += 1
    rec(idx+1, minus_cnt, t - value)

rec(0,0,t)
print(ans)