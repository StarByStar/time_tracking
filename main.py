from activity import Activity
import sqlite3
from tkinter import *


db = sqlite3.connect("database.db")
cursor = db.cursor()


def startActivity(activity_type):
    # Если активность еще не начата, создаем новую. Иначе - завершаем текущую
    print(Activity.running)
    if not Activity.running:
        global act
        act = Activity(1, activity_type)
        act.start_activity(cursor)
        db.commit()
    else:
        act.end_activity(cursor)
        db.commit()

def EndActivity():
    pass

# Начало цикла отрисовки
root = Tk()

# Заголовок
root.title("time tracking")

# Иконка
root.iconbitmap('mpv-icon.ico')

# функция для отключения кнопок
def ButtonDisabled(buttonName):
    if Activity.running:
        for button in buttonList:
            if button != buttonName:
                button['state'] = DISABLED
    else:
        ButtonEnabled()

def ButtonEnabled():
    if not Activity.running:
        for button in buttonList:
            button['state'] = NORMAL

# Элементы интерфейса
sleepLabel = Label(root, text="Sleep")
sleepButtonStart = Button(root, height=2, width=9, text="start / stop", command=lambda: (startActivity(1), ButtonDisabled(sleepButtonStart)))
sleepTimer = Label(root, text="XX")

trainingLabel = Label(root, text="Training")
trainingButtonStart = Button(root, height=2, width=9, text="start / stop", command=lambda: (startActivity(2), ButtonDisabled(trainingButtonStart)))
trainingTimer = Label(root, text="XX")

educationLabel = Label(root, text="Education")
educationButtonStart = Button(root, height=2, width=9, text="start / stop", command=lambda: (startActivity(3), ButtonDisabled(educationButtonStart)))
educationTimer = Label(root, text="XX")

entertainmentLabel = Label(root, text="Entertainment")
entertainmentButtonStart = Button(root, height=2, width=9, text="start / stop", command=lambda: (startActivity(4), ButtonDisabled(entertainmentButtonStart)))
entertainmentTimer = Label(root, text="XX")

# лист кнопок для управления их состоянием
buttonList = [sleepButtonStart, trainingButtonStart, educationButtonStart, entertainmentButtonStart]

# Разметка
sleepLabel.grid(row=3, column=1)
sleepButtonStart.grid(row=3, column=2)
sleepTimer.grid(row=3, column=4)

trainingLabel.grid(row=6, column=1)
trainingButtonStart.grid(row=6, column=2)
trainingTimer.grid(row=6, column=4)

educationLabel.grid(row=9, column=1)
educationButtonStart.grid(row=9, column=2)
educationTimer.grid(row=9, column=4)

entertainmentLabel.grid(row=12, column=1)
entertainmentButtonStart.grid(row=12, column=2)
entertainmentTimer.grid(row=12, column=4)


root.mainloop()



#sleep1 = Activity("Konstantin", "sleep", "03/01/2021 22:00")
# my_date = datetime.datetime.now()
# cursor.execute("INSERT INTO ACTIVITIES (USER_ID, START_DATE, ACTIVITY_TYPE) VALUES (?, ?, ?)", (1, my_date, 2))
# cursor.execute("UPDATE ACTIVITIES SET END_DATE = ? WHERE ID = ?", (datetime.datetime.now(), cursor.lastrowid))
# db.commit()
#
# cursor.execute("SELECT * from ACTIVITIES")
# #cursor.execute("SELECT last_insert_rowid()")
# print(cursor.lastrowid)
# print(cursor.fetchall())

# user = 1, activity = 3
# a = Activity(1, 3)
# a.start_activity(cursor)
# db.commit()
# time.sleep(20)
# a.end_activity(cursor)
# db.commit()

