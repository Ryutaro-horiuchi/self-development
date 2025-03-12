N=int(input())
A=map(int, input().split())

commodity = {'100': 0, '200': 0, '300': 0, '400': 0}
for amount in A:
  key = str(amount)
  commodity[key] += 1

print(commodity['100'] * commodity['400'] + commodity['200'] * commodity['300'])