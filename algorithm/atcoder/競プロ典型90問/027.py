N = int(input())

users = set()
for i in range(N):
    user = input()
    if user in users:
        continue
    else:
        users.add(user)
        print(i+1)