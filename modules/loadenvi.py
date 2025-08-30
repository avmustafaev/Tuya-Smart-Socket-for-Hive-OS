import os
from pathlib import Path
from dotenv import load_dotenv

class Envi:
    def __init__(self) -> None:
        # Загрузка .env файла только один раз с явным указанием пути
        env_path = Path(".") / ".env"
        load_dotenv(dotenv_path=env_path)
        
        # Получение переменных окружения с проверкой на наличие
        self.hiveos_api = self._get_env("HIVEOS_API")
        self.chat_id = self._get_env("CHAT_ID")
        self.tuya_api_key = self._get_env("TUYA_API_KEY")
        self.tuya_api_secret = self._get_env("TUYA_API_SECRET")
        self.tuya_region = self._get_env("TUYA_REGION")
        self.tuya_device_id = self._get_env("TUYA_DEVICE_ID")
        self.telegram_api = self._get_env("TELEGRAM_API")
        self.pause = int(self._get_env("PAUSE"))
        self.minutes_window = int(self._get_env("MINUTES_WINDOW"))

    def _get_env(self, key: str) -> str:
        """Вспомогательный метод для получения переменной окружения с проверкой"""
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Отсутствует обязательная переменная окружения: {key}")
        return value
