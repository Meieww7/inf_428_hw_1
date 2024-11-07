import numpy as np
import unittest

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)


def threat_score(data_by_department, importance_weights):
    weighted_sum = 0
    importance_sum = 0

    for scores, weight in zip(data_by_department, importance_weights):
        avg_score = np.mean(scores)  # среднее значение для department'а
        weighted_sum += avg_score * weight  # умножает на важность и добавляет к сумме
        importance_sum += weight  # суммирует вес department'а

    # Окончательный расчет aggregated score в диапазоне 0, 90
    if importance_sum == 0:
        return 0
    return min(90, max(0, weighted_sum / importance_sum))

class ThreatScoreTests(unittest.TestCase):
    # нет выбросов, не высокие оценки опасности
    def test_no_outliers(self):
        dep_data = [
            generate_random_data(30, 5, 50),
            generate_random_data(32, 5, 50),
            generate_random_data(31, 5, 50),
            generate_random_data(33, 5, 50),
            generate_random_data(29, 5, 50)
        ]
        importance_tags = [1, 1, 1, 1, 1]
        result = threat_score(dep_data, importance_tags)
        self.assertTrue(0 <= result <= 90)

    def test_mean_threat_scores(self):
        # у всех отделов похожие mean treat score, дисперсия небольшая
        departments_data = [
            generate_random_data(30, 3, 50),
            generate_random_data(31, 3, 50),
            generate_random_data(32, 3, 50),
            generate_random_data(29, 3, 50),
            generate_random_data(30, 3, 50)
        ]
        importance_tags = [1, 1, 1, 1, 1]
        result = threat_score(departments_data, importance_tags)
        self.assertTrue(0 <= result <= 90)  # проверка итогового балла в пределах допустимого диапазона


if __name__ == "__main__":
    unittest.main()
