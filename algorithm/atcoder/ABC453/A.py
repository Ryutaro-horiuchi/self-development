n = int(input())
s = input()
flag = True
for i in range(n):
    if s[i] == "o" and flag:
        continue
    elif s[i] != "o" and flag:
        flag = False
        print(s[i], end="")
    else:
        print(s[i], end="")
print("")