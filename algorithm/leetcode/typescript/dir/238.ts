function productExceptSelf(nums: number[]): number[] {
  let result: number[] = Array(nums.length).fill(1)

  let left = 1;
  for (let i = 0; i < nums.length; i++) {
    result[i] = left
    left *= nums[i]
  }

  let right = 1;
  for (let i = nums.length - 1; i >= 0; i--) {
    result[i] *= right;
    right *= nums[i];
  }

  return result
};

console.log(productExceptSelf([1,2,3,4]))

// 要素iを除く左側の積と右側の積を掛け合わせれば、O(n)で計算できると思います