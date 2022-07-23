import time

import tinytuya

import modules.settings as sett
from modules.connect_sql import sql_zapros as sqz


def select_sw(rig_id):
    sql_string = "SELECT rozetka_id, sw_name FROM hive2 WHERE rig_name = ?"
    return sqz(sql_string, (rig_id,))[0]


def do_rozetka(rig_id, doing):
    commands_off = ""
    commands_on = ""
    switch = select_sw(rig_id)
    sw_name = switch[1]
    roz_id = switch[0]
    print(roz_id, sw_name)
    if sw_name == "switch_1":
        commands_off = {
            "commands": [
                {"code": "switch_1", "value": False},
                {"code": "countdown_1", "value": 0},
            ]
        }
        commands_on = {
            "commands": [
                {"code": "switch_1", "value": True},
                {"code": "countdown_1", "value": 0},
            ]
        }
    elif sw_name == "switch":
        commands_off = {
            "commands": [
                {"code": "switch", "value": False},
                {"code": "countdown_1", "value": 0},
            ]
        }
        commands_on = {
            "commands": [
                {"code": "switch", "value": True},
                {"code": "countdown_1", "value": 0},
            ]
        }
    c = tinytuya.Cloud(
        sett.tuya_region, sett.tuya_api_key, sett.tuya_api_secret, roz_id
    )
    if doing == "reboot":
        result = c.sendcommand(roz_id, commands_off)
        print(doing, result)
        time.sleep(20)
        result = c.sendcommand(roz_id, commands_on)
        print(doing, result)
    if doing == "off":
        result = c.sendcommand(roz_id, commands_off)
        print(doing, result)
    if doing == "on":
        result = c.sendcommand(roz_id, commands_on)
        print(doing, result)
