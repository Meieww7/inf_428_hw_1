class Solution:
    def merge(self, nums1, m, nums2, n):
        temp = [] #временный массив для хранения результатов

        i, j = 0, 0  # указатели nums1 и nums2

        while i < m and j < n:  #тут будем сравнивать числа из nums1 и nums2
            if nums1[i] < nums2[j]:
                temp.append(nums1[i])
                i += 1
            else:
                temp.append(nums2[j])
                j += 1

        while i < m:  # тут копируем оставшиеся числа из nums1
            temp.append(nums1[i])
            i += 1

        while j < n: # тут копируем оставшиеся числа из nums2
            temp.append(nums2[j])
            j += 1

        for k in range(len(temp)): #копируем результат обратно в nums1
            nums1[k] = temp[k]


solution = Solution()
nums1 = [1, 2, 3, 0, 0, 0]
m = 3
nums2 = [2, 5, 6]
n = 3
solution.merge(nums1, m, nums2, n)
print(nums1)