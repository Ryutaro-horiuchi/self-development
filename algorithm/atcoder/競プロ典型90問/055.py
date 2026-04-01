import itertools

N,P,Q = map(int, input().split())
A = list(map(int, input().split()))

cnt = 0
for v in itertools.combinations(A, 5):
    if v[0] * v[1] % P * v[2] % P * v[3] % P * v[4] % P == Q:
        cnt+= 1
print(cnt)