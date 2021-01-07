from activity import Activity
import sqlite3
from datetime import datetime
from tkinter import *

db = sqlite3.connect("database.db")
cursor = db.cursor()

# Счетчик для таймера
sec = 0

# идентификатор действия для таймера
after_id = ''

# Параметры кнопок
h = 2
w = 9
btnName = "start / stop"


# Счетчик таймера
def tick():
    global sec, after_id, stopWatchDict
    after_id = root.after(1000, tick)
    f_sec = datetime.fromtimestamp(sec).strftime("%M:%S")
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
        # Запустить таймер
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


# Начать цикл отрисовки UI
root = Tk()

# Размер основной формы
root.geometry("300x250")

# Заголовок
root.title("time tracking")

# Иконка
root.iconbitmap('mpv-icon.ico')

# Элементы интерфейса
Timer = Label(root, font=("Courier", 44), text='00:00')

sleepLabel = Label(root, text="Sleep")
sleepButton = Button(root, height=h, width=w, text=btnName, command=lambda: (startActivity(1), changeBtnState(sleepButton)))

trainingLabel = Label(root, text="Training")
trainingButton = Button(root, height=h, width=w, text=btnName, command=lambda: (startActivity(2), changeBtnState(trainingButton)))

educationLabel = Label(root, text="Education")
educationButton = Button(root, height=h, width=w, text=btnName, command=lambda: (startActivity(3), changeBtnState(educationButton)))

entertainmentLabel = Label(root, text="Entertainment")
entertainmentButton = Button(root, height=h, width=w, text=btnName, command=lambda: (startActivity(4), changeBtnState(entertainmentButton)))

# лист кнопок для управления их состоянием
buttonList = [sleepButton, trainingButton, educationButton, entertainmentButton]

# Разметка
Timer.grid(row=1, column=1, columnspan=5)

sleepLabel.grid(row=2, column=1)
sleepButton.grid(row=3, column=1)

trainingLabel.grid(row=2, column=2)
trainingButton.grid(row=3, column=2)

educationLabel.grid(row=2, column=4)
educationButton.grid(row=3, column=4)

entertainmentLabel.grid(row=2, column=5)
entertainmentButton.grid(row=3, column=5)

root.mainloop()