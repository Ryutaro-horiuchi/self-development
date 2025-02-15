from functools import reduce

N = int(input())
nums = reduce(lambda x, y: x+y, map(int, input().split()))
print(nums % 100)
