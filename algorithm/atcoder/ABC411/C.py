N, Q = map(int, input().split())
cnt = 0
diff = [0 for _ in range(N+1)] # iとi+1の数値が違う場合、diff[i]は1である

for i in map(int, input().split()):
  if diff[i] == 0:
    diff[i] = 1
    cnt += 1
  else:
    diff[i] = 0
    cnt -= 1

  if diff[i-1] == 0:
    diff[i-1] = 1
    cnt += 1
  else:
    diff[i-1] = 0
    cnt -= 1 

  print(cnt // 2)
