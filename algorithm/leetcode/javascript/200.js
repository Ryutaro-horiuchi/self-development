/**
 * @param {character[][]} grid
 * @return {number}
 */
var numIslands = function(grid) {
  const m = grid.length // 行の数
  const n = grid[0].length // 列の数

  let visited = Array.from({length: m}, () => (Array(n).fill(false)))

  const dirs = [[1, 0], [0, -1], [-1, 0], [0, 1]]

  let count = 0;
  for (let y = 0; y < m; y++) {
    for (let x = 0; x < n; x++) {
      if ((visited[y][x]) || (grid[y][x] !== '1')) continue;
      count++
      dfs(x, y)
    }
  }

  return count

  function dfs(x, y){
    if ((x >= n || x < 0) || (y >= m || y < 0)) return;
    if (visited[y][x]) return;
    if (grid[y][x] !== '1') return;

    visited[y][x] = true
    
    dirs.forEach(([dx, dy]) => {
      let newX = x + dx
      let newY = y + dy

      dfs(newX, newY)
    })
  }
};

console.log(numIslands([
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]))