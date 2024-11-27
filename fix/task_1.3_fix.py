class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        set_nums1 = set(nums1)

        intersection = set()

        for num in nums2:
            if num in set_nums1:
                intersection.add(num)

        return list(intersection)
