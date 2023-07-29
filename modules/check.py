from datetime import datetime as dtime

from modules.lite_connector import sql_zapros as sqz
from modules.notifyer import add_notify
from modules.telega import do_telega
from modules.loadenvi import pause
from modules.wallet_onoff import pause_on

"""В этом модуле прописана вся логика
осталось ещё из модуля hiveosapi вынести лишгюю логику оттуда сюда
Как всё работает:
в модуле hiveosapi в цикле заполняется БД нынешней ситуацией в ферме и всё.
И функции этого модуля делают запросы в БД и таким образом в зависимости от ситуации с каждым ригом
обрабатывают логику работы всей системы
"""


def wakeuped():
    sql_string = (
        "SELECT rig_status, rig_name "
        "FROM hive2 "
        'WHERE rig_status != "working"  and rig_online = True'
    )
    rows = sqz(sql_string, ())
    for row in rows:
        if row[0] == "probably":
            add_notify(row[1], "self_heal")
        if row[0] == "rebooted":
            add_notify(row[1], "socket_healed")
        if row[0] == "emergency":
            add_notify(row[1], "heal_from_emergency")
    sql_string2 = (
        "UPDATE hive2 "
        'SET time = NULL , rig_status = "working" '
        'WHERE rig_status != "working"  and rig_online = True'
    )
    sqz(sql_string2, ())


def probably_sleeping():
    sql_string1 = (
        "SELECT rig_name "
        "FROM hive2 "
        'WHERE rozetka_exists = True and rig_status = "working"  '
        "and rig_online = False and is_watchdog = True"
    )
    rows = sqz(sql_string1, ())
    for row in rows:
        add_notify(row[0], "silent")
    sql_string2 = (
        "UPDATE hive2 "
        'SET time = ? , rig_status = "probably" '
        'WHERE rozetka_exists = True and rig_status = "working"  and rig_online = False'
    )
    sqz(sql_string2, (dtime.now(),))


def bez_rozetki():
    timenow = dtime.now()
    sql_string1 = (
        "SELECT rig_name, rig_id "
        "FROM hive2 "
        'WHERE rozetka_exists != True and rig_status = "working"  and rig_online = False'
    )
    rows = sqz(sql_string1, ())
    for row in rows:
        add_notify(row[0], "no_socket")
        sql_string2 = (
            "UPDATE hive2 "
            'SET time = ? , rig_status = "emergency" '
            "WHERE rig_id = ?"
        )
        sqz(sql_string2, (timenow, row[1]))


def rebooting():
    timenow = dtime.now()
    sql_string1 = (
        "SELECT time, rig_name, rozetka_id, rig_id "
        "FROM hive2 "
        'WHERE rozetka_exists = True and rig_status = "probably"  '
        "and rig_online = False and is_watchdog = True"
    )
    rows = sqz(sql_string1, ())
    for row in rows:
        if pause_on():
            do_telega("⏸ Поставлен на паузу!")
            break
        diff = timenow - dtime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
        print("time to reboot:", diff.seconds)
        if diff.seconds > pause:
            add_notify(row[1], "too_long_silent_reboot")
            sql_string2 = (
                "UPDATE hive2 "
                'SET time = ? , rig_status = "rebooted" '
                'WHERE rozetka_exists = True and rig_status = "probably" and '
                "rig_online = False and rig_id = ? "
            )
            sqz(sql_string2, (timenow, row[3]))


def re_problems():
    timenow = dtime.now()
    sql_string = (
        "SELECT rig_name, rozetka_id, rig_id "
        "FROM hive2 "
        "WHERE rozetka_exists = True and "
        "has_problems = True and rig_online = True and is_watchdog = True"
    )
    rows = sqz(sql_string, ())
    for row in rows:
        if pause_on():
            do_telega("⏸ Поставлен на паузу!")
            break
        add_notify(row[0], "has_problem_reboot")
        sql_string_2 = (
            "UPDATE hive2 "
            'SET time = ? , rig_status = "rebooted", has_problems = False '
            "WHERE rozetka_exists = True and rig_id = ? "
        )
        sqz(sql_string_2, (timenow, row[2]))


def do_emergency():
    timenow = dtime.now()
    sql_string = (
        "SELECT time, rig_name, rozetka_id, rig_id "
        "FROM hive2 "
        "WHERE rozetka_exists = True and "
        'rig_status = "rebooted"  and rig_online = False and is_watchdog = True'
    )
    rows = sqz(sql_string, ())
    for row in rows:
        if pause_on():
            do_telega("⏸ Поставлен на паузу!")
            break
        diff = timenow - dtime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
        print("time to shutdown:", diff.seconds)
        if diff.seconds > pause:
            add_notify(row[1], "is_emergency")
            sql_string_2 = (
                "UPDATE hive2 "
                'SET time = ? , rig_status = "emergency" '
                'WHERE rozetka_exists = True and rig_status = "rebooted"  and '
                "rig_online = False and rig_id = ? "
            )
            sqz(sql_string_2, (timenow, row[3]))


def unemergency():
    sql_string1 = (
        "SELECT rozetka_id, rig_name "
        "FROM hive2 "
        "WHERE rozetka_exists = True and "
        'rig_status = "emergency" and rig_online = False and is_watchdog = True'
    )
    rows = sqz(sql_string1, ())
    for row in rows:
        if pause_on():
            do_telega("⏸ Поставлен на паузу!")
            break
        add_notify(row[1], "heal_try")
