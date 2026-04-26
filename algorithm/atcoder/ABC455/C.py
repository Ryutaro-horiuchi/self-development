import heapq
from collections import defaultdict

n,k = map(int, input().split())
a = list(map(int, input().split()))

num = defaultdict(int)

for i in a:
    num[i] += 1

pq = []
for key, value in num.items():
    heapq.heappush(pq, -1*key*value)

try:
    [heapq.heappop(pq) for _ in range(k)]
except IndexError:
    pq = [0]

print(abs(sum(pq)))