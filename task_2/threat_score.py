import numpy as np
import unittest

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)


def threat_score(data_by_department):

    if not data_by_department or len(data_by_department) == 0:
        return 0  #нет данных значит 0

    all_users_scores = np.concatenate(data_by_department) # all level of угроз в один массив

    avg_score = np.mean(all_users_scores) # угрозалардын орташасы

    # Тут в общем проворачиваем махинации чтобы усилить влияние высоких уровней угроз (это особенно для 2 тесткейса)
    high_threat_threshold = np.percentile(all_users_scores, 75)
    high_threat_scores = all_users_scores[all_users_scores > high_threat_threshold]
    high_threat_boost = 0
    if len(high_threat_scores) > 0:
        high_threat_boost = np.mean(high_threat_scores) * 0.3

    final_score = avg_score + high_threat_boost # final расчет включает в себя mean value + вклад индивидуальных выбросов

    return min(90, max(0, final_score))

class ThreatScoreTests(unittest.TestCase):
    #All departments has quite same threat scores.
    def test_similar_threat_scores(self):
        dep_data = [
            generate_random_data(30, 5, 100),
            generate_random_data(32, 5, 100),
            generate_random_data(29, 5, 100),
            generate_random_data(31, 5, 100),
            generate_random_data(30, 5, 100)
        ]
        result = threat_score(dep_data)
        print(f"Final_case#1: {result}")
        self.assertTrue(30 <= result <= 50)


    def test_case2_one_high_department(self):
        # One department has a high score, other low => expected high threat score
        dep_data = [
            generate_random_data(10, 5, 100),
            generate_random_data(15, 5, 100),
            generate_random_data(20, 5, 100),
            generate_random_data(25, 5, 100),
            generate_random_data(85, 5, 100)
        ]
        result = threat_score(dep_data)
        print(f"Final_case#2: {result}")
        self.assertTrue(result > 40)

    def test_case3_high_threat_score_users(self):
        # All departments has the same mean threat score. BUT, in one department there are really high threat score users.
        dep_data = [
            generate_random_data(20, 5, 100),
            generate_random_data(25, 5, 100),
            generate_random_data(30, 5, 100),
            generate_random_data(35, 5, 100),
            np.concatenate([generate_random_data(30, 5, 95), np.array([85, 90, 90, 88, 87])])
        ]
        result = threat_score(dep_data)
        print(f"Final_case#3: {result}")
        self.assertTrue(result > 40)

    def test_case4_different_users(self):
        # All departments has a different number of users
        dep_data = [
            generate_random_data(40, 5, 34),
            generate_random_data(28, 5, 200),
            generate_random_data(12, 5, 78),
            generate_random_data(8, 5, 128),
            generate_random_data(30, 5, 174)
        ]
        result = threat_score(dep_data)
        print(f"Final_case#4: {result}")
        self.assertTrue(30 <= result <= 50)


if __name__ == "__main__":
    unittest.main()
