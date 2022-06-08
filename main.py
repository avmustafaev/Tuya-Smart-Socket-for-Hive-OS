from modules.connect_sql import db_not_exists, init_db
from modules.hiveosapi import getfarm
from modules.tuya import update_tuya_sockets
from modules.wallet_onoff import is_not_pause
from modules.check import wakeuped, probably_sleeping, rebooting, re_problems, do_emergency, bez_rozetki, unemergency
from time import sleep
from modules.settings import pause


def main():
    if db_not_exists():
        init_db()
        getfarm()
        update_tuya_sockets()
        
    while True:
        if is_not_pause():
            print('Скрипт в боевом режиме!')
            do_actions_sequence()
        print(f'Пауза {pause + 10} секунд , до следующей отработки цикла...')
        sleep(pause+10)


def do_actions_sequence():
    """Основная последовательность действий
    """
    getfarm()
    unemergency()
    wakeuped()
    probably_sleeping()
    rebooting()
    re_problems()
    do_emergency()
    bez_rozetki()


if __name__ == '__main__':
    main()
