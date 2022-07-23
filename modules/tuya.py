import tinytuya

import modules.settings as sett
from modules.connect_sql import sql_zapros as sqz


def update_tuya_sockets():
    device_id = ""
    device_key = ""
    device_name = ""

    c = tinytuya.Cloud(
        sett.tuya_region, sett.tuya_api_key, sett.tuya_api_secret, sett.tuya_device_id
    )
    devices = c.getdevices()

    for i in devices:
        device_name = i.get("name")
        device_id = i.get("id")
        device_key = i.get("key")
        sw_name = ""
        result = c.getstatus(device_id)["result"]
        for x in result:
            name = x.get("code")
            val = x.get("value")
            if name in ["switch_1", "switch"]:
                print(
                    f"☣️ smart socket: {device_name} | "
                    f"id:{device_id} | "
                    f"key:{device_key} | "
                    f"on:{str(val)} | "
                    f"code:{str(name)}"
                )
                sw_name = name
        tu = (sw_name, device_id, device_key, device_name)
        sql_string1 = (
            "UPDATE hive2 "
            "SET sw_name = ?, rozetka_id = ?, "
            "rozetka_key = ?, rozetka_exists = True where rig_name = ? "
        )
        sqz(sql_string1, tu)


if __name__ == "__main__":
    update_tuya_sockets()
