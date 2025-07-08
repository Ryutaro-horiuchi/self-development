S = list(input())
T = input()

uppers = []
for idx, value in enumerate(S[1:], start=1):
  if value.isupper():
    uppers.append(S[idx-1])

ans = "Yes"
for u in uppers:
  if u in T:
    continue
  else:
    ans = "No"
    break

print(ans)
