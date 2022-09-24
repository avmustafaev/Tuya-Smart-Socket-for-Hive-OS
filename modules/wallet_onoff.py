import os
import sys

from modules.connect_sql import sql_zapros as sqz
from modules.make_requests import hiveos_api_patch
from modules.make_requests import hiveos_requests_api as os_req_api
from modules.notifiyer import add_notify
from modules.send_to_telegram import do_telega

sys.path.insert(0, "./")

"""Глобальная проверка отключения отработки скрипта

В HiveOS создан кошелёк onoff
если адрес кошелька == 0 (равен нулю)
то скрипт не отрабатывает.
При любом другом значении скрипт отрабатывает,
удобно для обслуживания фермы целиком

"""


def get_wallet_info(wallet_name):
    sql_string = "SELECT farm_id " "FROM farms_id"
    ferm_id = sqz(sql_string, ())[0][0]
    wallet_response = os_req_api(f"{ferm_id}/wallets")["data"]
    for row in wallet_response:
        if row.get("name") == wallet_name:
            return row.get("id"), row.get("wal")
    do_telega(f"🔌 Кошелёк {wallet_name} не найден")
    return True


def wallet_parameter_true(wallet_name):
    try:
        int_parameter = int(get_wallet_info(wallet_name)[1])
    except ValueError:
        int_parameter = 1
    if int_parameter:
        return True
    return False


def need_update():
    if wallet_parameter_true("update_rigs_and_sockets"):
        do_telega("Вы запросили обновить БД")
        print("Вы запросили обновить БД")
        wallet_id = get_wallet_info("update_rigs_and_sockets")[0]
        print(wallet_id)
        hiveos_api_patch(wallet_id)
        os.remove(os.path.join("db", "data.db"))


def pause_on():
    sql_string = 'SELECT value FROM pref WHERE name="pause"'
    val_pause = sqz(sql_string, ())[0][0]
    if val_pause == "pause":
        return True
    elif val_pause == "unpause":
        return False


def is_not_pause():
    wallet_pause = not wallet_parameter_true("onoff")
    telega_pause = pause_on()
    bolik = not (wallet_pause or telega_pause)
    print(wallet_pause, telega_pause, bolik)
    if not bolik:
        do_telega("👨🏼‍🔧 Вся ферма на обслуживании, скрипт не отрабатывает")
        print("Скрипт на паузе")
        return False
    return True


def is_watchdoged(rig_watchdog_status, rig_name):
    if rig_watchdog_status is None:
        add_notify(rig_name, "no_watchdog")
        return False
    elif not rig_watchdog_status.get("enabled"):
        # Убрал оповещение о ватчдоге
        # add_notify(rig_name, "rig_ignored")
        return False
    return True


def rig_has_problems(rig_problems, rig_name):
    if rig_problems is None:
        return False
    isnt_prbmls = False
    for ii in rig_problems:
        if ii not in ["has_invalid", "error_message"]:
            add_notify(rig_name, ii)
            isnt_prbmls = ii != "overheat"
    return isnt_prbmls


if __name__ == "__main__":
    is_not_pause()
    # need_update()
