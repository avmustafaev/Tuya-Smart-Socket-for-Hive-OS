# compose.py
# Все импорты модулей
from modules.check import CheckUp
from modules.check_onoff import WalletPause
from modules.do_switch import DoSwitch
from modules.hive_api import HiveAPI
from modules.hive_sync import HiveSync
from modules.lite_connector import LiteConnector
from modules.loadenvi import Envi
from modules.my_tuya import MyTuya
from modules.notifyer import Notifyer
from modules.socket_pool_manage import SocketPoolManager
from modules.start_hour import StartHour
from modules.telega import SendTelega
from modules.trasfer2emergency import TransferToEmergency


class Compose:
    """Класс для инициализации и координации всех компонентов приложения"""
    
    def __init__(self):
        """Инициализация базовых зависимостей"""
        self.envi = Envi()  # Создаем экземпляр Envi сразу при инициализации
        
    def initialize_components(self):
        """Создает и возвращает инициализированные компоненты"""
        return {
            'check': CheckUp(self.envi),
            'wallet_pause': WalletPause(self.envi),
            'do_switch': DoSwitch(self.envi),
            'hive_api': HiveAPI(self.envi),
            'hive_sync': HiveSync(self.envi),
            'lite_connector': LiteConnector(self.envi),
            'my_tuya': MyTuya(self.envi),
            'notifyer': Notifyer(self.envi),
            'socket_pool': SocketPoolManager(self.envi),
            'start_hour': StartHour(self.envi),
            'telega': SendTelega(self.envi),
            'transfer_emergency': TransferToEmergency(self.envi)
        }
        
    def initialize_initial_steps(self, components):
        """
        Выполняет начальную инициализацию процессов
        Args:
            components: словарь инициализированных компонентов
        """
        # Пример последовательности инициализации
        components['hive_sync'].sync_data()
        components['socket_pool'].setup_pool()
        components['start_hour'].check_start_time()
        components['my_tuya'].update_devices()


# Пример использования в main.py
# from compose import Compose

# def main():
#     composer = Compose()
#     components = composer.initialize_components()
#     composer.initialize_initial_steps(components)
#     # Дальнейшая логика работы
