#from tinytuya import Cloud as tuyacloud

class MyTuya:
    def __init__(self, tuyaconnector, connector) -> None:
        self.tuya = tuyaconnector
        self.sqlreq = connector
        # self.update_tuya_sockets()

    def update_tuya_sockets(self):
        device_id = ""
        device_key = ""
        device_name = ""
        devices = self.tuya.getdevices()
        #print(devices)
        for i in devices:
            device_name = i.get('name')
            device_id = i.get('id')
            device_key = i.get('key')
            sw_name = ""
            result = self.tuya.getstatus(device_id)["result"]
            for x in result:
                name = x.get("code")
                print(name)
                #val = x.get("value")
                if name in ["switch_1", "switch"]:
                    # print(
                    #     f"☣️ smart socket: {device_name} | "
                    #     f"id:{device_id} | "
                    #     f"key:{device_key} | "
                    #     f"on:{str(val)} | "
                    #     f"code:{str(name)}"
                    # )
                    sw_name = name
                    break
            tu = (sw_name, device_id, device_key, device_name)
            sql_string1 = (
                "UPDATE hive2 "
                "SET sw_name = ?, rozetka_id = ?, "
                "rozetka_key = ?, rozetka_exists = True where rig_name = ? "
            )
            self.sqlreq(sql_string1, tu)
