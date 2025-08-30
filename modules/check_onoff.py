class WalletPause:
    def __init__(self, connector, os_req_api, telega, start_hour, notifyer) -> None:
        self.sqlreq = connector
        self.os_req_api = os_req_api
        self.telega = telega
        self.start_hour = start_hour
        self.add_notify = notifyer

    def get_wallet_info(self, wallet_name):
        # Упрощённая запись SQL-запроса
        sql_string = "SELECT farm_id FROM farms_id"
        ferm_id = self.sqlreq(sql_string, ())[0][0]
        
        wallet_response = self.os_req_api(f"{ferm_id}/wallets")["data"]
        
        # Используем генераторное выражение вместо цикла for
        result = next(
            (row.get("id"), row.get("wal")) 
            for row in wallet_response 
            if row.get("name") == wallet_name
        )
        
        if not result:
            self.telega(f"🔌 Кошелёк {wallet_name} не найден")
            return True  # Сомнительный возврат значения
        
        return result

    def wallet_parameter_true(self, wallet_name):
        # Добавлено исключение на случай, если get_wallet_info возвращает True
        try:
            value = self.get_wallet_info(wallet_name)
            if isinstance(value, bool):  # Проверка на булево значение
                return value
            int_parameter = int(value[1])
        except (ValueError, TypeError):
            int_parameter = 1
        return bool(int_parameter)

    def is_not_pause(self):
        wallet_pause = self.wallet_parameter_true("onoff")
        
        # Добавлена проверка, что start_hour - это функция
        if not wallet_pause:
            if callable(self.start_hour) and self.start_hour():
                self.telega("👨🏼‍🔧 Вся ферма на обслуживании, скрипт не отрабатывает")
            print("Скрипт на паузе")
            return False
        return True

    def is_watchdoged(self, rig_watchdog_status, rig_name):
        # Упрощена логика с использованием early return
        if rig_watchdog_status is None:
            self.add_notify(rig_name, "no_watchdog")
            return False
            
        if not rig_watchdog_status.get("enabled", False):
            self.add_notify(rig_name, "rig_ignored")
            return False
            
        return True

    def rig_has_problems(self, rig_problems, rig_name):
        # Упрощена логика и переименованы переменные
        if rig_problems is None:
            return False
            
        has_problems = False
        ignored_issues = [
            "has_invalid", "error_message", "no_hashrate",
            "missed_hashrate", "overload"
        ]
        
        for issue in rig_problems:
            if issue not in ignored_issues:
                print(issue)
                self.add_notify(rig_name, issue)
                has_problems = issue != "overheat"
                
        return has_problems
