"""
全ての長さが 3の数列(配列) 1から5までの数値を取る
"""


result = []
n, m = map(int, input().split())
for i in range(2**m):
    ans = []
    for idx, j in enumerate(range(1, m+1)):
        if ((i >> idx) & 1):
            ans.append(j)
    if len(ans) == n:
        result.append(ans)
result.sort()
for row in result:
    print(" ".join(map(str, row)))