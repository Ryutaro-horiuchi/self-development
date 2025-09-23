"use strict";
function maxSubArray(nums) {
    let currentSum = nums[0]; // -2
    let maxSum = nums[0]; // 1
    for (let i = 1; i < nums.length; i++) {
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        maxSum = Math.max(maxSum, currentSum);
    }
    return maxSum;
}
;
console.log(maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]));
// 開始位置と終了位置で2重にfor文を回す方法がまず考えられますが、O(N**2)になるので、パフォーマンスとしては良くない
// それまでの合計と、現在の要素のどちらが大きいかが考えられる。その値とこれまでの部分和の最大値のどちらが大きいかを求める
//# sourceMappingURL=53.js.map