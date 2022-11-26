import os
from pathlib import Path

from dotenv import load_dotenv

""" Модуль подтягивает параметры настроек из файла .env
и загружает в переменные окружения, затем из переменных окружения 
инициализирует настройки в переменные модуля
"""


load_dotenv()
env_path = Path(".") / ".env"
# print(env_path)
load_dotenv(dotenv_path=env_path)


telegram_chat_id = os.getenv("CHAT_ID")
print(telegram_chat_id)
tuya_api_key = os.getenv("TUYA_API_KEY")
tuya_api_secret = os.getenv("TUYA_API_SECRET")
tuya_region = os.getenv("TUYA_REGION")
print(tuya_region)
tuya_device_id = os.getenv("TUYA_DEVICE_ID")
telegram_api = os.getenv("TELEGRAM_API")
hiveos_api = os.getenv("HIVEOS_API")
pause = int(os.getenv("PAUSE"))
heroku_host = os.getenv("HEROKU_HOST")
heroku_db = os.getenv("HEROKU_DB")
heroku_user = os.getenv("HEROKU_USER")
heroku_password = os.getenv("HEROKU_PASSWORD")
heroku_port = os.getenv("HEROKU_PORT")
exb_access_key = os.getenv("EXB_AK")
exb_secret_key = os.getenv("EXB_SK")
minutes_window = int(os.getenv("MINUTES_WINDOW"))
print(f"В настройках установлена пауза: {pause} секунд\n")


def pauseunpause(value):
    os.environ["PAUSEUNPAUSE"] = value
    print(os.getenv("PAUSEUNPAUSE"))