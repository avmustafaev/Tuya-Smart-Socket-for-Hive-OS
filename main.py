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
from modules.hive_sync import getfarm
from modules.lite_connector import LiteConnector
from modules.loadenvi import Envi
from modules.my_tuya import update_tuya_sockets
from modules.notifyer import notify_constructor
from modules.socket_pool_manage import socket_manage
from modules.telega import do_telega
from modules.wallet_onoff import is_not_pause

envii = Envi()
litecon = LiteConnector()


def main():
    getfarm()
    update_tuya_sockets()
    while True:
        if is_not_pause():
            print("Скрипт в боевом режиме!")
            do_actions_sequence()
        print(f"Пауза {envii.pause + 10} секунд , до следующей отработки цикла...")
        sleep(envii.pause + 10)


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
    litecon.backup_db()


if __name__ == "__main__":
    do_telega("🚀 Запуск скрипта на сервере.. ")
    main()
