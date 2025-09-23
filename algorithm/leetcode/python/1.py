class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        ls = {}
        for idx, num in enumerate(nums):
            diff = target - num
            if diff in ls:
                return [ls[diff], idx]
            ls[num] = idx


if __name__ == "__main__":
    sol = Solution()
    print(sol.twoSum([2,7,11,15], 9))