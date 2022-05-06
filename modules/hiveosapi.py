from modules.connect_sql import sql_zapros as sqz
from modules.make_requests import hiveos_requests_api as os_req_api
from modules.telega import do_telega
from modules.if_has_octothorpe import del_octothorpe as del_oct
from modules.settings import telegram_chat_id as chat_id


"""Основной парсинг ответа из HiveOS
функция getfarm в цикле получает список ферм и заполняет таблицу в БД 
их ID и именами и в том же цикле запускает функцию getrig в которой передаёт имя
фермы и по нему получает список имён, ID, и остальные параметры ригов и заполняет
таблицу в БД этими данными
"""


def getrig(ferms_id):
    """Помимо получения списка ригов, их параметров
    в этой функции происходит проверка на включенный ватчдог
    и если он отключен происходит игнорирование присваивания аварийных статусов данному ригу
    на будущее этот механизм необхимо вынести из этой функции

    TODO игнорирование ватчдога оформить в отдельную функцию в модуле check.py

    Args:
        ferms_id для отработки функции обязательно в неё необходимо передать ID фермы в которой находится риг
    """
    ignore = False
    rig_response = os_req_api(f'{ferms_id}/workers?platform=1')['data']
    for i in rig_response:
        has_problems = False
        rig_name = del_oct(i.get('name'))
        rig_id = i.get('id')
        rig_stats = i.get('stats')
        # проверка watchdog тест от 30 03
        rig_wd = i.get('watchdog')
        if rig_wd is None:
            parttel = f'🪱 {rig_name}: настройте watchdog'
            do_telega(chat_id, parttel)
            ignore = True
        else:
            watchdoged = rig_wd.get('enabled')
        if not watchdoged:
            ignore = True
            partt = f'🛠 {rig_name}: на обслуживании не обращаю внимание на ошибки'
            do_telega(chat_id, partt)
        # проверка watchdog тест от 30 03
        online = rig_stats.get('online')
        problems = rig_stats.get('problems')
        if problems is not None and not ignore:
            for ii in problems:
                part = f'🤬 {rig_name}: {ii}'
                if ii not in ['has_invalid', 'error_message']:
                    print(rig_name)
                    print(ii)
                    do_telega(chat_id, part)
                    has_problems = True
        cort_upd = (chat_id,
                    rig_name,
                    online,
                    has_problems,
                    rig_id)
        cort_ins = (chat_id,
                    rig_id,
                    rig_name,
                    online,
                    '',
                    'working', '', '', '', '', '',
                    has_problems)
        sql_string1 = 'UPDATE hive2 SET chat_id=?, rig_name=?, rig_online = ?, has_problems = ? where rig_id = ?'
        sqz(sql_string1, cort_upd)
        sql_string2 = 'INSERT OR IGNORE INTO hive2 VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
        sqz(sql_string2, cort_ins)


# Функция посторочного запроса ферм из системы
def getfarm():
    """Функция получения списка ферм и их АйДи

    TODO вызов getrig вынести в отдельную функцию
    """
    farms_response = os_req_api('')['data']
    for a in farms_response:
        farm_name = a.get('name')
        farms_id = str(a.get('id'))
        sql_string1 = 'UPDATE farms_id SET farm_name = ? where farm_id = ? and chat_id = ?'
        sqz(sql_string1, (farm_name, farms_id, chat_id))
        sql_string2 = "INSERT OR IGNORE INTO farms_id VALUES (?,?,?)"
        sqz(sql_string2, (chat_id, farms_id, farm_name))
        getrig(farms_id)
