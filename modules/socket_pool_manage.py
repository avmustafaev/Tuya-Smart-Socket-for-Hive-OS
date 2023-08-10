import time


class SocketPoolManager:
    def __init__(
        self,
        sqlconnector,
        doswitch,
        transfer,
    ) -> None:
        self.request = sqlconnector
        self.do_rozetka = doswitch
        self.transfer = transfer

    def socket_manage(self):
        # self.manager_sql("has_problem_reboot", "reboot")
        # self.manager_sql("overheat", "off")
        # self.manager_sql("is_emergency", "off")
        # self.manager_sql("too_long_silent_reboot", "reboot")
        # self.manager_sql("heal_try", "reboot")
        self.manager_sql("overheat", "off")
        self.manager_sql("is_emergency", "off")
        self.manager_sql("has_problem_reboot", "off")
        self.manager_sql("too_long_silent_reboot", "off")
        self.manager_sql("heal_try", "off")
        time.sleep(20)
        self.manager_sql("has_problem_reboot", "on")
        self.manager_sql("too_long_silent_reboot", "on")
        self.manager_sql("heal_try", "on")
        self.request("DELETE FROM notify_pool", ())

    def manager_sql(self, notify_id, action):
        sql_string = "SELECT rig_id FROM notify_pool WHERE notify_id = ?"
        socket_pool = self.request(sql_string, (notify_id,))
        for socket in socket_pool:
            # if pause_on():
            #     do_telega("⏸ Поставлен на паузу!")
            #     break
            self.do_rozetka(socket[0], action)
            self.transfer(socket[0])
