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
            generate_random_data(30, 5, 128),
            generate_random_data(32, 5, 99),
            generate_random_data(31, 5, 10),
            generate_random_data(33, 5, 200),
            generate_random_data(29, 5, 163)
        ]
        importance_tags = [1, 2, 3, 4, 5]
        result = threat_score(dep_data, importance_tags)
        self.assertTrue(0 <= result <= 90)

    def test_mean_threat_scores(self):
        # у всех отделов похожие mean treat score, дисперсия небольшая
        # functional test
        departments_data = [
            generate_random_data(30, 3, 47),
            generate_random_data(31, 3, 94),
            generate_random_data(32, 3, 155),
            generate_random_data(29, 3, 50),
            generate_random_data(30, 3, 30)
        ]
        importance_tags = [5, 1, 4, 3, 2]
        result = threat_score(departments_data, importance_tags)
        self.assertTrue(0 <= result <= 90)  # проверка итогового балла в пределах допустимого диапазона

    def test_similar_number_of_users(self):
        # functional test
        dep_data = [
            generate_random_data(56, 5, 100),
            generate_random_data(32, 5, 100),
            generate_random_data(20, 5, 100),
            generate_random_data(87, 5, 100),
            generate_random_data(12, 5, 100)
        ]
        importance_tags = [4, 2, 1, 3, 5]
        result = threat_score(dep_data, importance_tags)
        self.assertTrue(0 <= result <= 90)

    def test_equal_importance(self):
        # unit test
        dep_data = [
            generate_random_data(56, 5, 41),
            generate_random_data(32, 5, 56),
            generate_random_data(20, 5, 189),
            generate_random_data(87, 5, 36),
            generate_random_data(12, 5, 18)
        ]
        importance_tags = [3, 3, 3, 3, 3]
        result = threat_score(dep_data, importance_tags)
        self.assertTrue(0 <= result <= 90)


    def test_threat_score_empty_input(self):
        #unit test
        dep_data = []
        importance_tags = []
        result = threat_score(dep_data, importance_tags)
        self.assertEqual(result, 0)


    def test_high_threat(self):
        # functional test
        dep_data = [
            generate_random_data(10, 5, 50),
            generate_random_data(15, 5, 50),
            generate_random_data(85, 5, 50),  # высокий уровень угрозы
            generate_random_data(20, 5, 50),
            generate_random_data(25, 5, 50)
        ]
        importance_tags = [1, 1, 5, 1, 1]  # максимальная важность департмента где угроза высокая
        result = threat_score(dep_data, importance_tags)
        self.assertTrue(result > 50)

if __name__ == "__main__":
    unittest.main()
