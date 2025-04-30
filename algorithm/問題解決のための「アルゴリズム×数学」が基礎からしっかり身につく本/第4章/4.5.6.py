import queue

R,C = map(int, input().split())
sy, sz = map(int, input().split())
gy, gz = map(int, input().split())

board = [list() for i in range(R)]
for i in range(R):
    board[i] = list(input())

count=1
for r in range(R):
    for c in range(C):
        if board[r][c] == '.':
          board[r][c] = count
          count+=1

G = [[] for i in range(count+1)]
for r in range(R):
    for c in range(C):
        if type(board[r][c]) == int:
            if type(board[r+1][c]) == int:
                G[board[r][c]].append(board[r+1][c])

            if type(board[r-1][c]) == int:
                G[board[r][c]].append(board[r-1][c])

            if type(board[r][c+1]) == int:
                G[board[r][c]].append(board[r][c+1])

            if type(board[r][c-1]) == int:
                G[board[r][c]].append(board[r][c-1])

dist = [-1] * (count+1)
Q = queue.Queue()
dist[board[sy-1][sz-1]] = 0
Q.put(board[sy-1][sz-1])

while not Q.empty():
    pos = Q.get()
    for next in G[pos]:
        if dist[next] == -1:
            dist[next] = dist[pos] + 1
            Q.put(next)

print(dist[board[gy-1][gz-1]])