class WalletPause:
    def __init__(self, connector, os_req_api, telega, start_hour, notifyer) -> None:
        self.sqlreq = connector
        self.os_req_api = os_req_api
        self.telega = telega
        self.start_hour = start_hour
        self.add_notify = notifyer

    def get_wallet_info(self, wallet_name):
        sql_string = "SELECT farm_id " "FROM farms_id"
        ferm_id = self.sqlreq(sql_string, ())[0][0]
        wallet_response = self.os_req_api(f"{ferm_id}/wallets")["data"]
        for row in wallet_response:
            if row.get("name") == wallet_name:
                return row.get("id"), row.get("wal")
        self.telega(f"🔌 Кошелёк {wallet_name} не найден")
        return True

    def wallet_parameter_true(self, wallet_name):
        try:
            int_parameter = int(self.get_wallet_info(wallet_name)[1])
        except ValueError:
            int_parameter = 1
        return bool(int_parameter)

    def is_not_pause(self):
        wallet_pause = self.wallet_parameter_true("onoff")
        if not wallet_pause:
            if self.start_hour():
                self.telega("👨🏼‍🔧 Вся ферма на обслуживании, скрипт не отрабатывает")
            print("Скрипт на паузе")
            return False
        return True

    def is_watchdoged(self, rig_watchdog_status, rig_name):
        if rig_watchdog_status is None:
            self.add_notify(rig_name, "no_watchdog")
            return False
        elif not rig_watchdog_status.get("enabled"):
            self.add_notify(rig_name, "rig_ignored")
            return False
        return True

    def rig_has_problems(self, rig_problems, rig_name):
        if rig_problems is None:
            return False
        isnt_prbmls = False
        for ii in rig_problems:
            if ii not in [
                "has_invalid",
                "error_message",
                "no_hashrate",
                "missed_hashrate",
                "overload",
            ]:  # , "overload",
                print(ii)
                self.add_notify(rig_name, ii)
                isnt_prbmls = ii != "overheat"
        return isnt_prbmls


""" def need_update():
    if wallet_parameter_true("update_rigs_and_sockets"):
        do_telega("Вы запросили обновить БД")
        print("Вы запросили обновить БД")
        wallet_id = get_wallet_info("update_rigs_and_sockets")[0]
        print(wallet_id)
        hiveos_api_patch(wallet_id)
        os.remove(os.path.join("db", "data.db")) """
