class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        seen = set()
        under_count = 0
        for num in nums:
            if num in seen:
                under_count += 1
                continue
            else:
                seen.add(num)

        nums = list(seen)
        nums.extend(["_"] * under_count)

        return len(seen)

if __name__ == "__main__":
    sol = Solution()
    print(sol.removeDuplicates([0,0,1,1,1,2,2,3,3,4]))