import json
from time import sleep
import requests
from modules.telega import SendTelega
from modules.loadenvi import Envi


class HiveAPI:
    def __init__(self, osapi) -> None:
        self.osapi = osapi
        self.envii = Envi()
        self.telegramer = SendTelega(self.envii)

    def hiveos_requests_api(self, requests_part, max_retries=5, timeout=10):
        url = "https://api2.hiveos.farm/api/v2/farms"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.osapi}",
        }
        url_full = f"{url}/{requests_part}" if requests_part else url

        print(f"[INFO] Запрос к HiveOS API: {url_full}")

        for attempt in range(1, max_retries + 1):
            try:
                print(f"[Попытка {attempt}/{max_retries}] Отправка запроса...")
                response = requests.get(url_full, headers=headers, timeout=timeout)

                if response.status_code == 200:
                    print("[УСПЕХ] Подключение к HiveOS API прошло успешно!")
                    self.telegramer.do_telega("Good connect to HiveOS API!")
                    return response.json()
                else:
                    print(f"[ОШИБКА HTTP] Код: {response.status_code}")
                    print(f"[ОТВЕТ ОТ СЕРВЕРА] {response.text[:300]}...")  # первые 300 символов
                    self.telegramer.do_telega(f"Ошибка API: {response.status_code}")

            except requests.exceptions.Timeout as e:
                print(f"[ТИМАУТ] Превышено время ожидания ответа: {e}")
                self.telegramer.do_telega("Таймаут запроса к API")

            except requests.exceptions.ConnectionError as e:
                print(f"[ОШИБКА СЕТИ] Не удалось подключиться: {e}")
                self.telegramer.do_telega("Ошибка подключения к API")

            except requests.exceptions.RequestException as e:
                print(f"[НЕИЗВЕСТНАЯ ОШИБКА REQUESTS] {e}")
                self.telegramer.do_telega("Неизвестная ошибка при запросе")

            except Exception as e:
                print(f"[КРИТИЧЕСКАЯ ОШИБКА] {type(e).__name__}: {e}")
                self.telegramer.do_telega("Критическая ошибка в запросе")

            # Ждём перед повтором, но не после последней попытки
            if attempt < max_retries:
                print("Ждём 10 секунд перед повторной попыткой...")
                sleep(10)

        # Все попытки закончились неудачей
        error_msg = "Не удалось подключиться к HiveOS API после всех попыток"
        print(f"[ПРОВАЛ] {error_msg}")
        self.telegramer.do_telega(error_msg)
        raise Exception(error_msg)

    def hiveos_api_patch(self, wallet_id):
        url = f"https://api2.hiveos.farm/api/v2/wallets/{wallet_id}"
        part = json.dumps({"wal": "0"})
        #print(part)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.osapi}",
        }
        return requests.patch(url, headers=headers, data=part)
