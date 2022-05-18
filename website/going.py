from flask import Blueprint
import sqlite3
import datetime
from time import sleep
import vk
from website import db
from website.models import Time

going = Blueprint('going', __name__)
APIVersion = 5.73

def get_status(vk_api, id):
    profiles = vk_api.users.get(user_id=id, fields='online, last_seen', v=APIVersion)
    if profiles[0]['online']:  # если появился в сети, то выводим время
        now = datetime.datetime.now()
        return 1, now.strftime("%d-%m-%Y %H:%M")
    if not profiles[0]['online']:  # если был онлайн, но уже вышел, то выводим время выхода
        return 2, datetime.datetime.fromtimestamp(profiles[0]['last_seen']['time']).strftime('%d-%m-%Y %H:%M')


def get_developer_info():
    try:
        sqlite_connection = sqlite3.connect('data_of_registration.db')
        cursor = sqlite_connection.cursor()

        sql_select_query = """select * from Note"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        for row in records:
            id = row[1]
            session = vk.Session(access_token='f63e74dd9a1d05dbf59707d202a6f98480b9cc1e1edca4da023b697723bf632a55357e4cec505547f458f')
            vk_api = vk.API(session)
            current_status, last_seen = get_status(vk_api, id)
            print(row[2], current_status, last_seen)
            last = a[row[0]]
            time_l = tim[row[0]]
            print(last, time_l)
            if last == 1 and current_status == 2:
                #db (from time_l to last_seen)
                new_time = Time(data=tim[row[0]], date=last_seen, note_id=row[0])
                db.session.add(new_time)
                db.session.commit()
                a[row[0]] = 0
            elif (last == None or last == 0) and current_status == 1:
                a[row[0]] = 1
                now = datetime.datetime.now()
                tim[row[0]] = now.strftime("%d-%m-%Y %H:%M")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


a = [0] * 100
tim = [0] * 100
while True:
    #get_developer_info()
    new_time = Time(data=tim[0], date=tim[1], note_id=1)
    db.session.add(new_time)
    db.session.commit()
    sleep(60)
