from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        if not nums or len(nums) == 0:
            return 0
        idex = 0
        for i, n in enumerate(nums):
            if n == val:
                continue
            n[idex] = n
            idex += 1


print(Solution().twoSum([3, 3], 6))
