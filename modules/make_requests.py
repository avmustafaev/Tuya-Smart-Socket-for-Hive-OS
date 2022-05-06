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
