import settings as sett
from hiveosapi import getfarm
from wallet_onoff import is_not_pause
from check import wakeuped, probably_sleeping, rebooting, re_problems, do_emergency, bez_rozetki, unemergency
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
    unemergency(sett.telegram_chat_id)
    wakeuped(sett.telegram_chat_id)
    probably_sleeping(sett.telegram_chat_id)
    rebooting(sett.telegram_chat_id)
    re_problems(sett.telegram_chat_id)
    do_emergency(sett.telegram_chat_id)
    bez_rozetki(sett.telegram_chat_id)


if __name__ == '__main__':
    main()
