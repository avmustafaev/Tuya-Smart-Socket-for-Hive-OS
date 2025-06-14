import os
from pathlib import Path

from dotenv import load_dotenv


class Envi:
    def __init__(self) -> None:
        load_dotenv()
        env_path = Path(".") / ".env"
        load_dotenv(dotenv_path=env_path)
        self.hiveos_api = os.getenv("HIVEOS_API")
        self.chat_id = os.getenv("CHAT_ID")
        self.tuya_api_key = str(os.getenv("TUYA_API_KEY"))
        self.tuya_api_secret = str(os.getenv("TUYA_API_SECRET"))
        self.tuya_region = str(os.getenv("TUYA_REGION"))
        self.tuya_device_id = str(os.getenv("TUYA_DEVICE_ID"))
        self.telegram_api = os.getenv("TELEGRAM_API")
        self.pause = int(os.getenv("PAUSE"))
        self.minutes_window = int(os.getenv("MINUTES_WINDOW"))


""" def pauseunpause(value):
    os.environ["PAUSEUNPAUSE"] = value
    print(os.getenv("PAUSEUNPAUSE")) """
