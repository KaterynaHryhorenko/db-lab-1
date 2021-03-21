URL = "https://zno.testportal.com.ua/yearstat/uploads/"
# Роки за які необхідно скачати дані ЗНО
YEARS = [2020, 2019]

# Файл де буде записана статистика
STATISTIC_CSV = "statistic.csv"

# Конфігурація під'єданання до БД
DB_NAME = "zno"
DB_USER = "postgres"
DB_PASS = "1111"
DB_PORT = "5432"
DB_HOST = "localhost"

# Симуляція некоректних даних у csv файлі
SIMULATE_ERROR = True
# Данні ЗНО за який рік потрібно пошкодити
SIMULATE_ERROR_YEAR = 2019
