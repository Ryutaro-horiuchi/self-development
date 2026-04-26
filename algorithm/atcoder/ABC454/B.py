n, m = map(int, input().split())
f = list(map(int, input().split()))

print("Yes" if len(set(f)) == len(f) else "No")
print("Yes" if len(set(f)) == m else "No")