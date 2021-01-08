from activity import Activity
import sqlite3
from datetime import datetime
from tkinter import *
import tkinter.ttk as ttk

db = sqlite3.connect("database.db")
cursor = db.cursor()

# идентификатор действия для таймера
after_id = ''

# Счетчик для таймера
sec = 0
mm = 58
hh = 0

# Параметры кнопок
h = 2
w = 10
btnName = "start / stop"


# Счетчик таймера
def tick():
    global after_id, sec, mm, hh
    after_id = root.after(1000, tick)
    if sec > 59:
        if mm >= 59:
            hh += 1
            mm = -1
        mm += 1
        sec = 0
    f_sec = str(hh) + ':' + str(mm) + ':' + str(sec)
    Timer['text'] = str(f_sec)
    sec += 1

# Завершить таймер
def stop_timer():
    root.after_cancel(after_id)


def startActivity(activity_type):
    # Если активность еще не начата, создаем новую. Иначе - завершаем текущую
    print(Activity.running)
    if not Activity.running:
        global act
        act = Activity(1, activity_type)
        act.start_activity(cursor, db)
    else:
        act.end_activity(cursor, db)


# функция для отключения кнопок
def changeBtnState(buttonName):
    if Activity.running:
        # Обнулить счетчик таймера, запустить таймер
        global sec, mm, hh
        sec = mm = hh = 0
        tick()
        # Отключить все кнопки кроме нажатой
        for button in buttonList:
            if button != buttonName:
                button['state'] = DISABLED
    else:
        # Включить все кнопки
        for button in buttonList:
            button['state'] = NORMAL
        # Остановить текущий запущенный таймер
        stop_timer()


# Функция сбора отчета , в параметрах передаются часы
def report(hours):
    activity_name ="Название активности"
    avg_duration = "Средняя продолжительность"
    avg_percent = "Средняя доля"
    avg_count = "Среднее кол-во"
    # Нужно прикрутить часы к выборке, в зависимости от типа вызванного отчета
    cursor.execute("SELECT DISTINCT AT.ACTIVITIES_NAME,"
                          " ROUND(SUM(CAST (STRFTIME('%s', ACTS.END_DATE) AS FLOAT) - STRFTIME('%s', ACTS.START_DATE) ) / 3600, 2) AS AVGTIME,"
                          " ROUND( (SUM(CAST (STRFTIME('%s', ACTS.END_DATE) AS FLOAT) - STRFTIME('%s', ACTS.START_DATE) ) / 3600) / 24 * 100, 2) AS AVGPERCENT,"
                          " COUNT( * ) AS CNT "
                          "FROM ACTIVITIES ACTS, "
                          "     ACTIVITIES_TYPES AT "
                          "WHERE 1 = 1 "
                          "     AND END_DATE > DATETIME('now', 'localtime', '-24 hours') "
                          "     AND ACTS.ACTIVITY_TYPE = AT.ID "
                          "GROUP BY AT.ACTIVITIES_NAME "
                          "ORDER BY AT.ACTIVITIES_NAME",)
    data = cursor.fetchall()

    # Начало цикла отрисовки формы с отчетом
    report = Tk()
    table = ttk.Treeview(report)

    for rec in data:
       table.insert('', 'end', values=rec)

    print(data)
    table["columns"] = [activity_name, avg_duration, avg_percent, avg_count]
    table["show"] = "headings"

    # Заголовки
    table.heading(activity_name, text=activity_name)
    table.heading(avg_duration, text=avg_duration)
    table.heading(avg_percent, text=avg_percent)
    table.heading(avg_count, text=avg_count)

    table.grid(row=1, column=1, columnspan=5)

    report.mainloop()

# Начать цикл отрисовки UI
root = Tk()

# Размер основной формы
root.geometry("402x250")

# Заголовок
root.title("time tracking")

# Иконка
root.iconbitmap('mpv-icon.ico')

# Элементы интерфейса
Timer = Label(root, font=("Courier", 50), text='0:0:0')

sleepLabel = Label(root, text="Sleep")
sleepButton = Button(root, height=h, width=w, text=btnName, command=lambda: (startActivity(1), changeBtnState(sleepButton)))

trainingLabel = Label(root, text="Training")
trainingButton = Button(root, height=h, width=w, text=btnName, command=lambda: (startActivity(2), changeBtnState(trainingButton)))

educationLabel = Label(root, text="Education")
educationButton = Button(root, height=h, width=w, text=btnName, command=lambda: (startActivity(3), changeBtnState(educationButton)))

entertainmentLabel = Label(root, text="Entertainment")
entertainmentButton = Button(root, height=h, width=w, text=btnName, command=lambda: (startActivity(4), changeBtnState(entertainmentButton)))

workLabel = Label(root, text="Work")
workButton = Button(root, height=h, width=w, text = btnName, command=lambda: (startActivity(5), changeBtnState(workButton)))

reportLabel = Label(root, font=("Courier", 24), text="Reports")
report1dButton = Button(root, height=h, width=w, text="1 day", command=lambda: (report(24)))
report7dButton = Button(root, height=h, width=w, text="7 days", command=lambda: (report(168)))
report30dButton = Button(root, height=h, width=w, text="30 days", command=lambda: (report(720)))


# лист кнопок для управления их состоянием
buttonList = [sleepButton, trainingButton, educationButton, entertainmentButton, workButton]

# Разметка
Timer.grid(row=1, column=1, columnspan=5)

sleepLabel.grid(row=2, column=1)
sleepButton.grid(row=3, column=1)

trainingLabel.grid(row=2, column=2)
trainingButton.grid(row=3, column=2)

workLabel.grid(row=2, column=3)
workButton.grid(row=3, column=3)

educationLabel.grid(row=2, column=4)
educationButton.grid(row=3, column=4)

entertainmentLabel.grid(row=2, column=5)
entertainmentButton.grid(row=3, column=5)

reportLabel.grid(row=4, column=1, columnspan=5)
report1dButton.grid(row=5, column=1)
report7dButton.grid(row=5, column=2)
report30dButton.grid(row=5, column=3)

root.mainloop()