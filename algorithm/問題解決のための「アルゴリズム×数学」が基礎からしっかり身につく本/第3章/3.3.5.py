def func(n, r):
  """nの中からr個を選択する数を返す"""
  numerator = 1
  denominator = 1
  for i in range(r):
    numerator *= (n - i)
    denominator *= (r - i)

  return int(numerator / denominator)

N=int(input())
A=map(int, input().split())

cards = {'1': 0, '2': 0, '3': 0}
for card in A:
  key = str(card)
  cards[key] += 1

ans = 0
for key, value in enumerate(cards):
  ans += func(int(value), 2)

print(ans)