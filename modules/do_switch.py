class DoSwitch:
    def __init__(self, sqlconnector, mytuya) -> None:
        self.sqlreq = sqlconnector
        self.mytuya = mytuya

    def select_sw(self, rig_id):
        # Добавлено исключение на случай пустого результата
        result = self.sqlreq("SELECT rozetka_id, sw_name FROM hive2 WHERE rig_name = ?", (rig_id,))
        if not result:
            raise ValueError(f"Не найдено устройство с rig_id: {rig_id}")
        return result[0]

    def do_rozetka(self, rig_id, doing):
        switch_data = self.select_sw(rig_id)
        roz_id, sw_name = switch_data
        
        # Единая конструкция для всех типов переключателей
        def create_commands(state):
            return {
                "commands": [
                    {"code": sw_name, "value": state},
                    {"code": "countdown_1", "value": 0}
                ]
            }

        if doing == "reboot":
            result_off = self.mytuya.sendcommand(roz_id, create_commands(False))
            print(f"{doing} - Выключение: {result_off}")
            
            # Добавлена явная задержка (раскомментирована и увеличена до 5 секунд)
            import time
            time.sleep(5)
            
            result_on = self.mytuya.sendcommand(roz_id, create_commands(True))
            print(f"{doing} - Включение: {result_on}")
            
        elif doing == "off":
            result = self.mytuya.sendcommand(roz_id, create_commands(False))
            print(f"{doing}: {result}")
            
        elif doing == "on":
            result = self.mytuya.sendcommand(roz_id, create_commands(True))
            print(f"{doing}: {result}")
