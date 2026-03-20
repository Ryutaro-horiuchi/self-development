X = int(input())

ans = 1
for i in range(2, X):
    x = i * i

    while x <= X:
        ans = max(ans, x)
        x *= i

print(ans)