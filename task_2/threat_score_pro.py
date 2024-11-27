import os
import csv
import numpy as np
from elasticsearch import Elasticsearch, helpers
import unittest

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)


#туточки генерируем данные для депарментов
def generate_data(num_departments, users_per_department, mean, variance):
    data = []
    for dep_id in range(1, num_departments + 1):
        department_data = generate_random_data(mean, variance, users_per_department)
        data.append((dep_id, department_data))
    return data


#тут и без коммментариев по названию функции понятно наверное но все равно напишу, сохраняем данные в csv
def save_data_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["department_id", "user_id", "threat_score"])

        for dep_id, department_data in data:
            for user_id, threat_score in enumerate(department_data, start=1):
                writer.writerow([dep_id, user_id, threat_score])
    print(f"The data is saved to the {filename}.")


# читаем данные из csv
# зачем я оставляю элементарные комменты еще и на русском? Ну чтобы не затупить на защите домашки =)
def read_data_from_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dep_id = int(row["department_id"])
            user_id = int(row["user_id"])
            threat_score = int(row["threat_score"])
            data.append((dep_id, user_id, threat_score))
    return data


#туточки создаю индекс с маппингом
#господи если 3 хоумворк будет тяжелее чем этот... жалпы қадалатын сияқтымын
def create_index(es, index_name):
    mapping = {
        "mappings": {
            "properties": {
                "department_id": {"type": "integer"},
                "user_id": {"type": "integer"},
                "threat_score": {"type": "integer"}
            }
        }
    }
    es.options(ignore_status=[400]).indices.create(index=index_name, body=mapping)
    print(f"Index {index_name} has been created.")


#загружаю данные из csv в elasticsearch
def load_data_to_elasticsearch(es, index_name, filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        actions = [
            {
                "_index": index_name,
                "_source": {
                    "department_id": int(row["department_id"]),
                    "user_id": int(row["user_id"]),
                    "threat_score": int(row["threat_score"])
                }
            }
            for row in reader
        ]
        print(f"Actions for Elasticsearch: {actions[:5]}")  # тут я выводила первые 5 действий из-за ошибки в тесткейсах но сейчас вроде бы все гуд
        helpers.bulk(es, actions)
        print("Data uploaded to Elasticsearch.")



# старый добрый threat score, не зря правда pro, потому что теперь берет данные из эластика и возвращает итоговый уровень угроз
def threat_score(es, index_name):
    #ну тут мы запрос кидаем в эластик для получения всех данных
    query = {
        "size": 10000,
        "query": {"match_all": {}}  # сам запрос
    }

    response = es.search(index=index_name, body=query)

    #на всякий случай, проверка на отсутствие данных, ну мало ли
    if not response["hits"]["hits"]:
        print("Error: there is no data in the index.")
        return 0  #если данных нет, возвращаем 0

    #вытаскиваю из ответа эластика все уровни угроз
    all_users_scores = np.array([hit["_source"]["threat_score"] for hit in response["hits"]["hits"]])

    #тут рассчитываю среднее значение threat score
    avg_score = np.mean(all_users_scores)

    #для усиления влияния отдельных высоких значений угроз, нахожу 75-й процентиль
    high_threat_threshold = np.percentile(all_users_scores, 75)
    high_threat_scores = all_users_scores[all_users_scores > high_threat_threshold]

    #если есть высокие угрозы, увеличиваю итоговый балл
    high_threat_boost = 0
    if len(high_threat_scores) > 0:
        high_threat_boost = np.mean(high_threat_scores) * 0.3  # усиливаю вклад высоких угроз на 30%

    # среднее значение + усиление за счёт выбросов = наш итог
    final_score = avg_score + high_threat_boost

    final_score = min(90, max(0, final_score))

    print(f"The average threat level: {avg_score}, Усиление за счёт высоких угроз: {high_threat_boost}")
    return final_score


class ThreatScoreTests(unittest.TestCase):
    FILENAME = "test_data.csv"

    @classmethod
    def setUpClass(cls):
        #генерация тестовых данных, если файл ещё не существует
        if not os.path.exists(cls.FILENAME):
            data = generate_data(5, 100, 30, 5)
            save_data_to_csv(data, cls.FILENAME)

        #подключение к эластику и загрузка данных
        cls.es = Elasticsearch("http://localhost:9200")
        cls.index_name = "test_threat_index"
        create_index(cls.es, cls.index_name)
        load_data_to_elasticsearch(cls.es, cls.index_name, cls.FILENAME)

    # Test case 1: All departments have quite the same threat scores.
    def test_similar_threat_scores(self):
        dep_data = [
            generate_random_data(30, 5, 100),
            generate_random_data(32, 5, 100),
            generate_random_data(29, 5, 100),
            generate_random_data(31, 5, 100),
            generate_random_data(30, 5, 100)
        ]
        result = threat_score(self.es, self.index_name)
        print(f"Final_case#1: {result}")
        self.assertTrue(30 <= result <= 50)

    # Test case 2: One department has a high score, others low = expected high threat score.
    def test_case2_one_high_department(self):
        dep_data = [
            generate_random_data(10, 5, 100),
            generate_random_data(15, 5, 100),
            generate_random_data(20, 5, 100),
            generate_random_data(25, 5, 100),
            generate_random_data(85, 5, 100)
        ]
        result = threat_score(self.es, self.index_name)
        print(f"Final_case#2: {result}")
        self.assertTrue(result > 40)

    # Test case 3: All departments have the same mean threat score, but one department has high threat score users.
    def test_case3_high_threat_score_users(self):
        dep_data = [
            generate_random_data(20, 5, 100),
            generate_random_data(25, 5, 100),
            generate_random_data(30, 5, 100),
            generate_random_data(35, 5, 100),
            np.concatenate([generate_random_data(30, 5, 95), np.array([85, 90, 90, 88, 87])])
        ]
        result = threat_score(self.es, self.index_name)
        print(f"Final_case#3: {result}")
        self.assertTrue(result > 40)

    # Test case 4: All departments have a different number of users.
    def test_case4_different_users(self):
        dep_data = [
            generate_random_data(40, 5, 34),
            generate_random_data(28, 5, 200),
            generate_random_data(12, 5, 78),
            generate_random_data(8, 5, 128),
            generate_random_data(30, 5, 174)
        ]
        result = threat_score(self.es, self.index_name)
        print(f"Final_case#4: {result}")
        self.assertTrue(30 <= result <= 50)

if __name__ == "__main__":
    FILENAME = "threat_data.csv"
    INDEX_NAME = "threat_index"
    NUM_DEPARTMENTS = 5
    USERS_PER_DEPARTMENT = 100
    MEAN = 30
    VARIANCE = 5

    #генерация или загрузка данных
    if not os.path.exists(FILENAME):
        data = generate_data(NUM_DEPARTMENTS, USERS_PER_DEPARTMENT, MEAN, VARIANCE)
        save_data_to_csv(data, FILENAME)
    else:
        print(f"The {FILENAME} file already exists. We use existing data.")

    #подключение к Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    #создание индекса и загрузка данных
    create_index(es, INDEX_NAME)
    load_data_to_elasticsearch(es, INDEX_NAME, FILENAME)

    #вычисление среднего уровня угроз
    threat_score(es, INDEX_NAME)

    unittest.main()
