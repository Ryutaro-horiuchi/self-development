h, w = map(int, input().split())

grid = ["_" * (w+1)]
for _ in range(h):
    grid.append("_"+input())


ans = 0
for h1 in range(1, h+1):
    for h2 in range(1, h+1):
        if h1 > h2:
            continue

        for w1 in range(1, w+1):
            for w2 in range(1, w+1):
                if w1 > w2:
                    continue

                ok = True
                for i in range(h1, h2+1):
                    for j in range(w1, w2+1):
                        if grid[i][j] != grid[h1+h2-i][w1+w2-j]:
                            ok = False
                            break
                    if not ok:
                        False
                if ok:
                    ans += 1

print(ans)