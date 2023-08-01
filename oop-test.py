from time import sleep

import tinytuya

from modules.check import CheckUp
from modules.check_onoff import WalletPause
from modules.do_switch import DoSwitch
from modules.hive_sync import HiveSync
from modules.lite_connector import LiteConnector
from modules.loadenvi import Envi
from modules.my_tuya import MyTuya
from modules.notifyer import Notifyer
from modules.socket_pool_manage import SocketPoolManager
from modules.start_hour import StartHour
from modules.telega import SendTelega


def main():
    envii = Envi()
    telegramer = SendTelega(envii)
    telegramer.do_telega("🚀 Запуск скрипта на сервере.. ")
    starthour = StartHour(envii.minutes_window)
    litecon = LiteConnector()
    notify = Notifyer(
        litecon,
        telegramer,
        starthour,
    )
    checkup = CheckUp(
        litecon.request,
        notify.add_notify,
        telegramer.do_telega,
        envii.pause,
        False,
    )
    hivesync = HiveSync(
        litecon,
        envii.hiveos_api,
        notify,
    )
    tuyaconnector = tinytuya.Cloud(
        envii.tuya_region,
        envii.tuya_api_key,
        envii.tuya_api_secret,
        envii.tuya_device_id,
    )
    onoff = WalletPause(
        litecon.request,
        hivesync.hiveos_requests_api,
        telegramer.do_telega,
        starthour.start_hour,
        notify.add_notify,
    )
    mytuya = MyTuya(tuyaconnector, litecon.request)
    do_switcher = DoSwitch(
        litecon.request,
        mytuya,
    )
    socket_manager = SocketPoolManager(litecon.request, do_switcher.do_rozetka)
    mytuya.update_tuya_sockets()
    litecon.backup_db()

    while True:
        if onoff.is_not_pause():
            _extracted_from_main_43(checkup, notify, litecon, socket_manager)
        print(f"Пауза {envii.pause + 10} секунд , до следующей отработки цикла...")
        sleep(envii.pause + 10)


# TODO Rename this here and in `main`
def _extracted_from_main_43(checkup, notify, litecon, socketmanager):
    print("Скрипт в боевом режиме!")
    checkup.unemergency()
    checkup.wakeuped()
    checkup.probably_sleeping()
    checkup.rebooting()
    checkup.re_problems()
    checkup.do_emergency()
    checkup.bez_rozetki()
    notify.notify_constructor()
    socketmanager.socket_manage()
    litecon.backup_db()


if __name__ == "__main__":
    main()
