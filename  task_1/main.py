class Solution(object):
    def findLengthOfLCIS(self, nums):

        max_length = 1
        start = 0

        for i in range(1, len(nums)):
            if nums[i] <= nums[i - 1]:
                max_length = max(max_length, i - start)
                start = i

                return max(max_length, len(nums) - start)

solution = Solution()

nums1 = [1, 3, 5, 4, 7]
result1 = solution.findLengthOfLCIS(nums1)
print(f"Result for nums1: {result1}")

nums2 = [2, 2, 2, 2, 2]
result2 = solution.findLengthOfLCIS(nums2)
print(f"Result for nums2: {result2}")
