N = int(input())
A = list(map(int, input().split()))

cuts = [0]
p = 0
for c in A:
    p += c
    p %= 360
    cuts.append(p)

cuts.append(360)
cuts.sort()

c = 0
for i in range(1, len(cuts)):
    c = max(c, cuts[i]-cuts[i-1])
print(c)
