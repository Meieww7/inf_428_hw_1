class Solution:
    def intersection(self, nums1, nums2):
        #превращаем список в сет
        set1 = set(nums1)
        set2 = set(nums2)
        result = set()

        for num in set1:
            if num in set2:
                result.add(num)


        return list(result) # возвращаем список

solution = Solution()
print(solution.intersection([1, 2, 2, 1], [2, 2]))
print(solution.intersection([4, 9, 5], [9, 4, 9, 8, 4]))
