import requests
from modules.settings import telegram_api as tel_api
from modules.settings import telegram_chat_id as chat_id

""" В модуле две функции имеющих отношение к Telegram

Первая просто запрашивает Чат Айди, причём из БД
на всякий случай на будущее это сделано если один скрипт будет обрабатывать несколько ферм разных владельцев

Вторая функция напрямую без библиотек отправляет сообщения в телеграм бота. Максимально просто.

"""

def do_telega(part):
    requests.get(f'https://api.telegram.org/bot{tel_api}/sendMessage?text={part}&chat_id={chat_id}')
