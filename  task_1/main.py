class Solution(object):
    def findLengthOfLCIS(self, nums):

        max_length = 1 #тут хранится максимальная длина
        start = 0 # эта переменная считает начало последовательности

        for i in range(1, len(nums)):
            if nums[i] <= nums[i - 1]: # конец последовательности
                max_length = max(max_length, i - start) # вычисляем длину этой последовательности и обновляем переменную где хранится максимальная длина
                start = i #перемещаем на текущий индекс чтобы начать отслеживать новую последовательность

        return max(max_length, len(nums) - start) # проверяем последнюю последовательность так как она может быть самой длинной

solution = Solution()

nums1 = [1, 3, 5, 4, 7]
result1 = solution.findLengthOfLCIS(nums1)
print(f"Result for nums1: {result1}")

nums2 = [2, 2, 2, 2, 2]
result2 = solution.findLengthOfLCIS(nums2)
print(f"Result for nums2: {result2}")
