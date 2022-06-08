import os
from dotenv import load_dotenv
from pathlib import Path

""" Модуль подтягивает параметры настроек из файла .env
и загружает в переменные окружения, затем из переменных окружения 
инициализирует настройки в переменные модуля
"""


load_dotenv()
env_path = Path('.')/'.env'
# print(env_path)
load_dotenv(dotenv_path=env_path)


telegram_chat_id = os.getenv('CHAT_ID')
print(telegram_chat_id)
tuya_api_key = os.getenv('TUYA_API_KEY')
tuya_api_secret = os.getenv('TUYA_API_SECRET')
tuya_region = os.getenv('TUYA_REGION')
print(tuya_region)
tuya_device_id = os.getenv('TUYA_DEVICE_ID')
telegram_api = os.getenv('TELEGRAM_API')
hiveos_api = os.getenv('HIVEOS_API')
pause = int(os.getenv('PAUSE'))
print(f'В настройках установлена пауза: {pause} секунд\n')
