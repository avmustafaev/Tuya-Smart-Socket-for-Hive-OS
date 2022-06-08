from modules.connect_sql import sql_zapros as sqz
from modules.make_requests import hiveos_requests_api as os_req_api
from modules.make_requests import getfarms_api, getrigs_api
from modules.if_has_octothorpe import del_octothorpe as del_oct
from modules.wallet_onoff import rig_has_problems, is_watchdoged


"""Основной парсинг ответа из HiveOS
функция getfarm в цикле получает список ферм и заполняет таблицу в БД 
их ID и именами и в том же цикле запускает функцию getrig в которой передаёт имя
фермы и по нему получает список имён, ID, и остальные параметры ригов и заполняет
таблицу в БД этими данными
"""


def getrig(ferms_id):
    rig_response = getrigs_api(ferms_id)
    sql_upd_string = 'UPDATE hive2 ' \
                     'SET rig_name=?, rig_online = ?, is_watchdog = ?, has_problems = ? ' \
                     'WHERE rig_id = ?'
    sql_ins_ignore_str = 'INSERT OR IGNORE INTO hive2 VALUES (?,?,?,?,?,?,?,?,?,?,?)'
    
    for i in rig_response:
        rig_name = del_oct(i.get('name'))
        rig_stats = i.get('stats')
        is_online = rig_stats.get('online')
        is_watchdog_on = is_watchdoged(i.get('watchdog'), rig_name)
        has_problems = rig_has_problems(rig_stats.get('problems'), rig_name)
        rig_id = i.get('id')
        cort_upd = (rig_name,
                    is_online,
                    is_watchdog_on,
                    has_problems,
                    rig_id)
        cort_ins = (rig_id,
                    rig_name,
                    is_online,
                    '',
                    'working', '', '', 
                    is_watchdog_on, 
                    '', '',
                    has_problems)
        sqz(sql_upd_string, cort_upd)
        sqz(sql_ins_ignore_str, cort_ins)


# Функция посторочного запроса ферм из системы
def getfarm():
    """Функция получения списка ферм и их АйДи

    TODO вызов getrig вынести в отдельную функцию
    """
    farms_response = getfarms_api()
    sql_string1 = 'UPDATE farms_id SET farm_name = ? where farm_id = ?'
    sql_string2 = 'INSERT OR IGNORE INTO farms_id VALUES (?,?)'
    for a in farms_response:
        farm_name = a.get('name')
        farms_id = str(a.get('id'))
        sqz(sql_string1, (farm_name, farms_id))
        sqz(sql_string2, (farms_id, farm_name))
        getrig(farms_id)
