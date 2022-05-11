from modules.send_to_telegram import do_telega
from modules.make_requests import hiveos_requests_api as os_req_api
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
                 'FROM farms_id'
    ferm_id = sqz(sql_string, ())[0][0]
    wallet_response = os_req_api(f'{ferm_id}/wallets')['data']
    for row in wallet_response:
        if row.get('name') == 'onoff':
            return check_onoff_wallet(row.get('id'), ferm_id)
    do_telega('🔌 Кошелёк onoff не найден, поэтому пауза не проверяется')
    return True


def check_onoff_wallet(onoff_wallet_id, ferm_id):
    try:
        int_onoff = int(os_req_api(
            f'{ferm_id}/wallets/{onoff_wallet_id}').get('wal'))
    except ValueError:
        int_onoff = 33
    if int_onoff:
        return True
    do_telega('👨🏼‍🔧 Вся ферма на обслуживании, скрипт не отрабатывает')
    print('Скрипт на паузе')
    return False


def is_watchdoged(rig_watchdog_status, rig_name):
    if rig_watchdog_status is None:
        return compile_send_telegram('🪱 ', rig_name, ': настройте watchdog', False)
    elif not rig_watchdog_status.get('enabled'):
        return compile_send_telegram('🛠 ', rig_name, ': на обслуживании не обращаю внимание на ошибки', False)
    return True


def compile_send_telegram(emotion, rig_name, message, bool_response):
    part = f'{emotion}{rig_name}{message}'
    print(part)
    do_telega(part)
    return bool_response


def rig_has_problems(rig_problems, rig_name):
    if rig_problems is not None:
        isnt_prbmls = False
        for ii in rig_problems:
            if ii not in ['has_invalid', 'error_message']:
                isnt_prbmls = compile_send_telegram('🤬 ', rig_name, f': {ii}', True)
        return isnt_prbmls
    return False


if __name__ == '__main__':
    print(is_not_pause())
