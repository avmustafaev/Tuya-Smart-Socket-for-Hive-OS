import requests
import settings as sett

"""В модуле одна функция
которая делает запрос в HiveOS API
и возвращает ответ в json
"""


def hiveos_requests_api(requests_part):
    url = 'https://api2.hiveos.farm/api/v2/farms'
    bear = f"Bearer {sett.hiveos_api}"
    headers = {'Content-Type': 'application/json', 'Authorization': bear}
    url_full = f'{url}/{requests_part}' if requests_part != '' else url
    response_from_api = requests.get(url_full, headers=headers)
    return response_from_api.json()
