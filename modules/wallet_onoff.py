from telega import do_telega
from make_requests import hiveos_requests_api as os_req_api
import settings as sett


"""Глобальная проверка отключения отработки скрипта

В HiveOS создан кошелёк onoff
если адрес кошелька == 0 (равен нулю)
то скрипт не отрабатывает.
При любом другом значении скрипт отрабатывает,
удобно для обслуживания фермы целиком

"""

def is_not_pause():
    """Функция возвращает True если адрес кошелька onoff не равен нулю
    
    TODO сделать отдельную функцию которая будет искать кошелёк onoff
    и получать его id
    """
    try:
        int_onoff = int(os_req_api('1935712/wallets/5968598').get('wal'))
    except ValueError:
        int_onoff = 33
    if int_onoff:
        return True
    do_telega(sett.telegram_chat_id, '👨🏼‍🔧 Вся ферма на обслуживании, скрипт не отрабатывает')
    print('Скрипт на паузе')
    return False