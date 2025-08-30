class MyTuya:
    def __init__(self, tuyaconnector, connector) -> None:
        self.tuya = tuyaconnector
        self.sqlreq = connector
        self.update_tuya_sockets()

    def update_tuya_sockets(self):
        """Обновляет данные о розетках Tuya в БД"""
        target_switches = {"switch_1", "switch"}  # Оптимизация поиска
        
        devices = self.tuya.getdevices()
        
        for device in devices:
            device_info = {
                'name': device.get('name'),
                'id': device.get('id'),
                'key': device.get('key')
            }
            
            try:
                status_result = self.tuya.getstatus(device_info['id'])["result"]
                
                # Ищем актуальный switch code
                active_switch = next(
                    (item for item in status_result 
                     if item.get("code") in target_switches),
                    None
                )
                
                if active_switch:
                    update_data = (
                        active_switch["code"],
                        device_info['id'],
                        device_info['key'],
                        device_info['name']
                    )
                    
                    sql_query = (
                        "UPDATE hive2 "
                        "SET sw_name = ?, rozetka_id = ?, "
                        "rozetka_key = ?, rozetka_exists = True "
                        "WHERE rig_name = ?"
                    )
                    
                    self.sqlreq(sql_query, update_data)
                    
            except Exception as e:
                # Лучше использовать логгер вместо print
                print(f"Ошибка обработки устройства {device_info['name']}: {str(e)}")
