h,w = map(int, input().split())
for i in range(h):
    for j in range(w):
        if i == 0 or i == h-1:
            print("#"*w)
            break
        if j == 0:
            print("#", end="")
        elif j == w-1:
            print("#")
        else:
            print(".", end="")