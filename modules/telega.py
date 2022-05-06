import requests
from connect_sql import sql_zapros as sqz
import settings as sett

""" В модуле две функции имеющих отношение к Telegram

Первая просто запрашивает Чат Айди, причём из БД
на всякий случай на будущее это сделано если один скрипт будет обрабатывать несколько ферм разных владельцев

Вторая функция напрямую без библиотек отправляет сообщения в телеграм бота. Максимально просто.

"""

def get_telega():
    return str(sqz('SELECT chat_id FROM chat_id WHERE activnost = ?', (1,))[0][0])


def do_telega(t_chat_id, part):
    requests.get(f'https://api.telegram.org/bot{sett.telegram_api}/sendMessage?text={part}&chat_id={t_chat_id}')
