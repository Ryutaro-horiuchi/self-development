N=int(input())
A=map(int, input().split())

cards = {}

for number in A:
  key = str(number)
  if cards.get(key):
    cards[key] += 1
    continue
  cards[key] = 1

ans = 0
for number_key, n_sheets in cards.items():
  other_number_key = str(100000 - int(number_key))
  if not cards.get(other_number_key):
    continue

  if number_key == '50000':
    ans += int(cards[other_number_key] * (cards[other_number_key] - 1) // 2)
    continue

  ans += cards[other_number_key] * cards[number_key]
  cards[other_number_key] = 0

print(ans)