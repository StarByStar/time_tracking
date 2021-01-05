import datetime

# класс отслеживаемых активностей
class Activity:
    running = True

    # Конструктор
    def __init__(self, user_id, activity_type):
        self.user = user_id
        self.activity_type = activity_type
        # текущая дата и время начала
        self.start_date = datetime.datetime.now()

    # для теста "перегрузки" операций
    def __repr__(self):
        return 'activity: %s, %s, %s, %s' % (self.user, self.activity_type, self.start_date)

# Установить для записи о начатой активности дату и время окончания
    def end_activity(self, cursor):
        # текущая дата и время завершения
        self.end_date = datetime.datetime.now()
        self.running = False
        # id последней записи в рамках сессии (надо переделать)
        id = cursor.lastrowid
        cursor.execute("UPDATE ACTIVITIES SET END_DATE = ? WHERE ID = ?", (self.end_date, id))

# Создать в базе запись о начале активности
    def start_activity(self, cursor):
        cursor.execute("INSERT INTO ACTIVITIES "
                       "(USER_ID, START_DATE, ACTIVITY_TYPE) VALUES (?, ?, ?)",
                       (self.user, self.start_date, self.activity_type))

# Проверка активности
    def isrunning(self):
        return self.running


# Вывод тестов только когда запускаем сам файл
# Не выводим тесты, если файл с классом импортируется
# if __name__ == '__main__':
#     # тесты
#     sleep1 = Activity("Konstantin", "sleep", "03/01/2021 22:00")
#     work = Activity("Konstantin", "work", "03/01/2021 16:00", "03/01/2021 22:00")
#     print(sleep1)
#     print(work)
#     work.kek = 3
#     Activity.kek = 2
#     print(work.kek)