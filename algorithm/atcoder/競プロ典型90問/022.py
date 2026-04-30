a,b,c, = map(int, input().split())


def gcd(a, b):
    while b:
        a, b = b, a % b

    return a

ab = gcd(a, b)
g = gcd(ab, c)

print(a//g + b//g + c//g - 3)
