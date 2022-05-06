from modules.telega import do_telega
from modules.make_requests import hiveos_requests_api as os_req_api
from modules.settings import telegram_chat_id as chat_id
from modules.connect_sql import sql_zapros as sqz


"""Глобальная проверка отключения отработки скрипта

В HiveOS создан кошелёк onoff
если адрес кошелька == 0 (равен нулю)
то скрипт не отрабатывает.
При любом другом значении скрипт отрабатывает,
удобно для обслуживания фермы целиком

"""


def is_not_pause():
    # Получение id кошелька onoff
    sql_string = 'SELECT farm_id ' \
                 'FROM farms_id ' \
                 'WHERE chat_id = ? '
    ferm_id = sqz(sql_string, (chat_id,))[0][0]
    wallet_response = os_req_api(f'{ferm_id}/wallets')['data']
    for row in wallet_response:
        if row.get('name') == 'onoff':
            return check_onoff_wallet(row.get('id'), ferm_id)
    do_telega(chat_id, '🔌 Кошелёк onoff не найден, поэтому пауза не проверяется')
    return True


def check_onoff_wallet(onoff_wallet_id, ferm_id):
    try:
        int_onoff = int(os_req_api(
            f'{ferm_id}/wallets/{onoff_wallet_id}').get('wal'))
    except ValueError:
        int_onoff = 33
    if int_onoff:
        return True
    do_telega(chat_id, '👨🏼‍🔧 Вся ферма на обслуживании, скрипт не отрабатывает')
    print('Скрипт на паузе')
    return False


if __name__ == '__main__':
    print(is_not_pause())
