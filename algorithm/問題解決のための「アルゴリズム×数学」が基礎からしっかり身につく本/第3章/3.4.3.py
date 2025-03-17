N=int(input())
A=list(map(int, input().split()))
B=list(map(int, input().split()))

ans=0
for i in range(N):
  ans += A[i] / 3
  ans += B[i] / 3 * 2

print(ans)