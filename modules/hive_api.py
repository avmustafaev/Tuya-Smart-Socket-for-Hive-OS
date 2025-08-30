import json
import logging
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from modules.telega import SendTelega
from modules.loadenvi import Envi


class HiveAPI:
    def __init__(self, osapi) -> None:
        self.osapi = osapi
        self.envii = Envi()
        self.telegramer = SendTelega(self.envii)
        
        # Настройка логгирования вместо print
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _create_session(self):
        """Создает сессию с настройками повторных попыток"""
        session = requests.Session()
        retry = Retry(
            total=5,  # Максимум 5 попыток
            backoff_factor=2,  # Экспоненциальный backoff (1s, 2s, 4s, 8s, 16s)
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        return session
    
    def hiveos_requests_api(self, requests_part):
        """
        Улучшенный метод запроса к HiveOS API с:
        - Повторными попытками с экспоненциальным backoff
        - Логированием вместо print
        - Обработкой исключений
        """
        session = self._create_session()
        url = "https://api2.hiveos.farm/api/v2/farms"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.osapi}",
        }
        url_full = f"{url}/{requests_part}" if requests_part != "" else url
        
        try:
            response_from_api = session.get(url_full, headers=headers, timeout=10)
            response_from_api.raise_for_status()  # Вызовит исключение при 4xx/5xx
            self.logger.info("Успешное подключение к HiveOS API")
            return response_from_api.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ошибка запроса: {e}")
            self.telegramer.do_telega(f"Критическая ошибка API: {str(e)}")
            raise

    def hiveos_api_patch(self, wallet_id, payload=None):
        """
        PATCH-запрос с улучшениями:
        - Гибкий параметр payload
        - Лучшая обработка ответа
        - JSON сериализация
        """
        url = f"https://api2.hiveos.farm/api/v2/wallets/{wallet_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.osapi}",
        }
        
        # Используем переданный payload или значение по умолчанию
        data = json.dumps(payload) if payload else json.dumps({"wal": "0"})
        
        try:
            response = requests.patch(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            self.logger.info(f"PATCH-запрос успешен: {response.status_code}")
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP-ошибка PATCH: {e.response.status_code}")
            self.telegramer.do_telega(f"Ошибка обновления кошелька: {e}")
            return None
