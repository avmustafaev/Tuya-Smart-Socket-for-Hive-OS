import sys

from modules.lite_connector import sql_zapros as sqz
from modules.hive_sync import getfarm
from modules.my_tuya import update_tuya_sockets

# Удаление текущей директории из пути (необязательно, если структура проекта корректна)
sys.path.insert(0, "./")

try:
    # Очистка таблиц перед обновлением данных
    sqz("DELETE FROM hive2", ())  # Удаление старых записей из таблицы hive2
    sqz("DELETE FROM farms_id", ())  # Очистка таблицы farms_id
    
    # Обновление данных из Hive
    getfarm()  # Получение актуальных данных ферм
    
    # Синхронизация с Tuya
    update_tuya_sockets()  # Обновление состояния розеток Tuya
    
except Exception as e:
    print(f"Ошибка при выполнении операций: {e}")
    # Логирование ошибки или дополнительные действия по восстановлению
