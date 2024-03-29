import json

import requests


class HiveAPI:
    def __init__(self, osapi) -> None:
        self.osapi = osapi

    def hiveos_requests_api(self, requests_part):
        url = "https://api2.hiveos.farm/api/v2/farms"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.osapi}",
        }
        url_full = f"{url}/{requests_part}" if requests_part != "" else url
        response_from_api = requests.get(url_full, headers=headers)
        return response_from_api.json()

    def hiveos_api_patch(self, wallet_id):
        url = f"https://api2.hiveos.farm/api/v2/wallets/{wallet_id}"
        part = json.dumps({"wal": "0"})
        print(part)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.osapi}",
        }
        return requests.patch(url, headers=headers, data=part)
