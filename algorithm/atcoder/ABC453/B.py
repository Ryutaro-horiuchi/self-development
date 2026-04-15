t,x = map(int, input().split())
a = list(map(int, input().split()))

last = 0
for index, value in enumerate(a):
    if index == 0 or abs(last - value) >= x:
        last = value
        print(f"{index} {value}")
