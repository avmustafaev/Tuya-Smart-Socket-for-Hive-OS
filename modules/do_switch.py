# import time


class DoSwitch:
    def __init__(self, sqlconnector, mytuya) -> None:
        self.sqlreq = sqlconnector
        self.mytuya = mytuya

    def select_sw(self, rig_id):
        sql_string = "SELECT rozetka_id, sw_name FROM hive2 WHERE rig_name = ?"
        return self.sqlreq(sql_string, (rig_id,))[0]

    def do_rozetka(self, rig_id, doing):
        commands_off = ""
        commands_on = ""
        switch = self.select_sw(rig_id)
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
        if doing == "reboot":
            result = self.mytuya.sendcommand(roz_id, commands_off)
            print(doing, result)
            # time.sleep(20)
            # result = self.mytuya.sendcommand(roz_id, commands_on)
            print(doing, result)
        if doing == "off":
            result = self.mytuya.sendcommand(roz_id, commands_off)
            print(doing, result)
        if doing == "on":
            result = self.mytuya.sendcommand(roz_id, commands_on)
            print(doing, result)
