function twoSum(nums: number[], target: number): number[] {
  const map = new Map<number, number>();

  for (let i=0; i < nums.length; i++) {
    const num = nums[i]
    const diff = target - num
    if (map.has(diff)) {
      return [map.get(diff) as number, i]
    }

    map.set(num, i)
  }

  return [1,2]
};

console.log(twoSum([2,7,11,15], 9))

/**
 * numsを先頭から順に走査して組み合わせを探索する方法があるが、最大でnums.length分の累乗を回す必要があり、問題文からN**1000(nums.length)になるので、効率がわるい
 * 出てきた値とインデックスをMapで保持。for文でnumsを回していき、すでに出てきている値とnumの合計がtargetになればそれで終了。計算量はO(nums.length)になる。
 */