from modules.check_onoff import pause_on
from modules.func import do_rozetka
from modules.lite_connector import sql_zapros as sqz
from modules.telega import do_telega


def manager_sql(notify_id, action):
    sql_string = "SELECT rig_id FROM notify_pool WHERE notify_id = ?"
    socket_pool = sqz(sql_string, (notify_id,))
    print(socket_pool)
    for socket in socket_pool:
        if pause_on():
            do_telega("⏸ Поставлен на паузу!")
            break
        do_rozetka(socket[0], action)


def socket_manage():
    manager_sql("has_problem_reboot", "reboot")
    manager_sql("overheat", "off")
    manager_sql("is_emergency", "off")
    manager_sql("too_long_silent_reboot", "reboot")
    manager_sql("heal_try", "reboot")
    sqz("DELETE FROM notify_pool", ())
