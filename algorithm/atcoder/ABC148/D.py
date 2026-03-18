N = int(input())
A = list(map(int, input().split()))

cnt = 1
ans = 0

for i in A:
    if i == cnt:
        cnt+=1
    else:
        ans+=1

print(-1 if ans == N else ans)