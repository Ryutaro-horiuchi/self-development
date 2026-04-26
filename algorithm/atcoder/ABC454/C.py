from queue import Queue
N, M = map(int, input().split())

G = [[] for _ in range(N+1)]

for i in range(M):
	u, v = map(int, input().split())
	G[u].append(v)

def bfs(G, s):
    que = Queue()

    visited = [False] * (N + 1)

    que.put(s)
    visited[s] = True

    while not que.empty():
        v = que.get()
        for v2 in G[v]:
            if visited[v2] == True:
                continue

            que.put(v2)
            visited[v2] = True

    return visited

visited = bfs(G, 1)
print(sum(visited))
