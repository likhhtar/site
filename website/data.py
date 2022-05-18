import datetime
from time import sleep
import vk

APIVersion = 5.73

def get_status(current_status, vk_api, id):
    profiles = vk_api.users.get(user_id=id, fields='online, last_seen', v=APIVersion)
    if profiles[0]['online']:  # если появился в сети, то выводим время
        now = datetime.datetime.now()
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Появился в сети в: ', now.strftime("%d-%m-%Y %H:%M"))
        return True
    if not profiles[0]['online']:  # если был онлайн, но уже вышел, то выводим время выхода
        print('Вышел из сети: ', datetime.datetime.fromtimestamp(profiles[0]['last_seen']['time']).strftime('%d-%m-%Y %H:%M'))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        return False
    return current_status

def get_name(vk_api, id):
    profiles = vk_api.users.get(user_ids=id,fields='first_name, last_name', v=APIVersion)
    return profiles[0]['first_name'] + ' ' + profiles[0]['last_name']

if __name__ == '__main__':
    id = input("Имя пользователя в ссылке на его страницу(vk.com/XXXXXXXXX): ")
    session = vk.Session(access_token='f63e74dd9a1d05dbf59707d202a6f98480b9cc1e1edca4da023b697723bf632a55357e4cec505547f458f')
    vk_api = vk.API(session)
    print(get_name(vk_api, id))
    current_status = False
    while(True):
        current_status = get_status(current_status, vk_api, id)
        sleep(60)
