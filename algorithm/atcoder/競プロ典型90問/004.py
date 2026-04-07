H, W = map(int, input().split())

grid = [[0 for _ in range(W)] for _ in range(H+1)]

for i in range(H):
    h = list(map(int, input().split()))
    grid[i] = [*h, sum(h)]
    for j in range(W):
        grid[H][j] += grid[i][j]

for i in range(H):
    for j in range(W):
        print(grid[-1][j] + grid[i][-1] - grid[i][j], end=" ")
    print("")