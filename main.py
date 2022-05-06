from modules.settings import telegram_chat_id as chat_id
from modules.hiveosapi import getfarm
from modules.wallet_onoff import is_not_pause
from modules.check import wakeuped, probably_sleeping, rebooting, re_problems, do_emergency, bez_rozetki, unemergency
from time import sleep


def main():
    while True:
        if is_not_pause():
            print('Скрипт в боевом режиме!')
            do_actions_sequence()
        print('Пауза 610 секунд , до следующей отработки цикла...')
        sleep(610)


def do_actions_sequence():
    """Основная последовательность действий
    """
    getfarm()
    unemergency(chat_id)
    wakeuped(chat_id)
    probably_sleeping(chat_id)
    rebooting(chat_id)
    re_problems(chat_id)
    do_emergency(chat_id)
    bez_rozetki(chat_id)


if __name__ == '__main__':
    main()
