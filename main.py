from time import sleep

from modules.check import (
    bez_rozetki,
    do_emergency,
    probably_sleeping,
    re_problems,
    rebooting,
    unemergency,
    wakeuped,
)
from modules.connect_sql import backup_db, db_not_exists, init_db
from modules.get_exbitron import get_exbitron
from modules.hiveosapi import getfarm
from modules.notifiyer import notify_constructor
from modules.send_to_telegram import do_telega
from modules.settings import pause
from modules.socket_pool_manage import socket_manage
from modules.tuya import update_tuya_sockets
from modules.wallet_onoff import is_not_pause


def main():
    print(get_exbitron())
    if db_not_exists():
        print("Создаётся пустая БД")
        init_db()
        print("Запрашивается список ферм")
        getfarm()
        update_tuya_sockets()

    while True:
        if is_not_pause():
            print("Скрипт в боевом режиме!")
            do_actions_sequence()
        print(f"Пауза {pause + 10} секунд , до следующей отработки цикла...")
        sleep(pause + 10)


def do_actions_sequence():
    """Основная последовательность действий"""
    getfarm()
    unemergency()
    wakeuped()
    probably_sleeping()
    rebooting()
    re_problems()
    do_emergency()
    bez_rozetki()
    notify_constructor()
    socket_manage()
    backup_db()


if __name__ == "__main__":
    do_telega("🚀 Запуск скрипта на сервере.. ")
    main()
