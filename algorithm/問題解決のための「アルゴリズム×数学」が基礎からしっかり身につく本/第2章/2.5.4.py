def is_prime(n):
  for i in range(2, n):
    if n % i == 0:
      return False

  return True

N=int(input())
prime = []
for i in range(2, N+1):
  if is_prime(i):
    prime.append(i)

print(*prime)