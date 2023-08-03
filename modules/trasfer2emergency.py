import json

import requests


class TransferToEmergency:
    def __init__(
        self,
        osapi,
        sqlconn,
        telega,
    ) -> None:
        self.osapi = osapi
        self.sqlreq = sqlconn
        self.do_telega = telega

    def transfer(self, rig_name):
        rig_id, farm_id = self._get_farm_id(rig_name)
        if int(farm_id) != 1935712:
            part = f"🛠️ Переносим риг: {rig_name} в раздел Emergency"
            print(part)
            self.do_telega(part)
            print(self._api_patch(rig_id, farm_id))
        else:
            print("Переносить не нужно", rig_name)

    def _api_patch(self, rig_name, farm_id):
        url = f"https://api2.hiveos.farm/api/v2/farms/{farm_id}/workers/{rig_name}/transfer"
        part = json.dumps({"target_farm_id": 1935712})
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.osapi}",
        }
        return requests.post(url, headers=headers, data=part)

    def _get_farm_id(self, rig_name):
        sql_string = "SELECT rig_id, farm_id FROM hive2 WHERE rig_name=?"
        req = self.sqlreq(sql_string, (rig_name,))[0]
        return req[0], req[1]
