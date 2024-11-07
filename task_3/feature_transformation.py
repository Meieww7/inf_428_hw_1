#
# def time_difference(time_1, time_2):
#     diff = abs(time_1 - time_2)
#     return min(diff, 24 - diff)
#
# print(time_difference(23, 1))

import numpy as np
import unittest


def time_to_cyclic_features(hour):

    if hour < 0 or hour >= 24:
        raise ValueError("Hour must be between 0 and 24")

    sin_feature = np.sin(2 * np.pi * hour / 24)  #преобразование времени в синус
    cos_feature = np.cos(2 * np.pi * hour / 24)  #преобразование времени в косинус

    return sin_feature, cos_feature


class TestFeatureTransformation(unittest.TestCase):

    def test_time_features(self):
        # проверка для разных временных значений
        test_cases = [
            (0, (0, 1)),  # проверка на начало дня, тут синус 0 косинус 1
            (6, (np.sin(2 * np.pi * 6 / 24), np.cos(2 * np.pi * 6 / 24))),  # проверка для 6 часов синус и косинус по формуле
            (12, (0, -1)),  # полдень проверка синус 0 кос -1
            (18, (np.sin(2 * np.pi * 18 / 24), np.cos(2 * np.pi * 18 / 24))),  # проверка для 18 часов
            (23, (np.sin(2 * np.pi * 23 / 24), np.cos(2 * np.pi * 23 / 24)))  # на конец дня проверочка
        ]

        # для проверки каждого часа из кейса независимо
        for hour, expected in test_cases:
            with self.subTest(hour=hour):
                result = time_to_cyclic_features(hour)
                self.assertAlmostEqual(result[0], expected[0], places=5)
                self.assertAlmostEqual(result[1], expected[1], places=5)

    def test_invalid_hour(self):
        # проверка для некорректных значений времени типо -1 или 24 00
        with self.assertRaises(ValueError):
            time_to_cyclic_features(-1)
        with self.assertRaises(ValueError):
            time_to_cyclic_features(24)


if __name__ == "__main__":
    unittest.main()
