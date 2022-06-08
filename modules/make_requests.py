import json
import requests
from modules.settings import hiveos_api as os_api

"""В модуле одна функция
которая делает запрос в HiveOS API
и возвращает ответ в json
"""


def hiveos_requests_api(requests_part):
    url = 'https://api2.hiveos.farm/api/v2/farms'
    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {os_api}"}
    url_full = f'{url}/{requests_part}' if requests_part != '' else url
    response_from_api = requests.get(url_full, headers=headers)
    return response_from_api.json()


def hiveos_api_patch(wallet_id):
    url = f'https://api2.hiveos.farm/api/v2/wallets/{wallet_id}'
    part = json.dumps({
        'wal':'0'
        })
    print(part)
    headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {os_api}"}
    return requests.patch(url, headers=headers, data=part)



def getfarms_api():
    return hiveos_requests_api('')['data']


def getrigs_api(ferms_id):
    return hiveos_requests_api(f'{ferms_id}/workers?platform=1')['data']