N = int(input())
S = input()

left = [0] * (N)
cache = set()
for i in range(N):
    cache.add(S[i])
    left[i] = cache.copy()


right = [0] * N
cache = set()
for i in range(-1, -N-1, -1):
    cache.add(S[i])
    right[i] = cache.copy()

ans = 0
for i in range(1,N-1):
    ans = max(ans, len(left[i] & right[i+1]))

print(ans)
