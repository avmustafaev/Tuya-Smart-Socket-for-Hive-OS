from modules.func import do_rozetka
from modules.connect_sql import sql_zapros as sqz
from modules.telega import do_telega
from datetime import datetime as dtime

"""В этом модуле прописана вся логика
осталось ещё из модуля hiveosapi вынести лишгюю логику оттуда сюда
Как всё работает:
в модуле hiveosapi в цикле заполняется БД нынешней ситуацией в ферме и всё.
И функции этого модуля делают запросы в БД и таким образом в зависимости от ситуации с каждым ригом
обрабатывают логику работы всей системы
"""


def wakeuped(t_chat_id):
    emo = ''
    event_rig = ''
    sql_string = 'SELECT rig_status, rig_name ' \
                 'FROM hive2 ' \
                 'WHERE rig_status != "working"  and rig_online = True and chat_id = ? '
    rows = sqz(sql_string, (t_chat_id,))
    for row in rows:
        if row[0] == 'probably':
            do_telega(t_chat_id, f'🌱 {row[1]}: ожил сам')
        if row[0] == 'rebooted':
            do_telega(t_chat_id, f'☘️ {row[1]}: розеточка помогла! перезагрузился!')
        if row[0] == 'emergency':
            do_telega(t_chat_id, f'🍀 {row[1]}: восстановлен из аварийных')
    sql_string2 = 'UPDATE hive2 ' \
                  'SET time = NULL , rig_status = "working" ' \
                  'WHERE rig_status != "working"  and rig_online = True and chat_id = ?'
    sqz(sql_string2, (t_chat_id,))


def probably_sleeping(t_chat_id):
    sql_string1 = 'SELECT rig_name ' \
                  'FROM hive2 ' \
                  'WHERE rozetka_exists = True and rig_status = "working"  ' \
                  'and rig_online = False and chat_id = ? and is_watchdog = True'
    rows = sqz(sql_string1, (t_chat_id,))
    for row in rows:
        part = f'🤐 {row[0]}: молчит, даём 10 минут, может обновляется или перезагружается?'
        do_telega(t_chat_id, part)
    sql_string2 = 'UPDATE hive2 ' \
                  'SET time = ? , rig_status = "probably" ' \
                  'WHERE rozetka_exists = True and rig_status = "working"  and rig_online = False and chat_id = ? '
    sqz(sql_string2, (dtime.now(), t_chat_id,))


def bez_rozetki(t_chat_id):
    timenow = dtime.now()
    sql_string1 = 'SELECT rig_name, rig_id ' \
                  'FROM hive2 ' \
                  'WHERE rozetka_exists != True and rig_status = "working"  and rig_online = False and chat_id = ? '
    rows = sqz(sql_string1, (t_chat_id,))
    for row in rows:
        part = f'🚫 {row[0]}: Нет розетки! Сразу перевожу в аварийный статус!'
        do_telega(t_chat_id, part)
        sql_string2 = 'UPDATE hive2 ' \
                      'SET time = ? , rig_status = "emergency" ' \
                      'WHERE chat_id = ? and rig_id = ?'
        sqz(sql_string2, (timenow, t_chat_id, row[1]))


def rebooting(t_chat_id):
    timenow = dtime.now()
    sql_string1 = 'SELECT time, rig_name, rozetka_id, rig_id ' \
                  'FROM hive2 ' \
                  'WHERE rozetka_exists = True and rig_status = "probably"  ' \
                  'and rig_online = False and chat_id = ? and is_watchdog = True'
    rows = sqz(sql_string1, (t_chat_id,))
    for row in rows:
        diff = timenow - dtime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
        print('time to reboot:', diff.seconds)
        if diff.seconds > 600:
            part = f'♻️ {row[1]}: молчит больше 10 минут — перезагружаем...'
            do_telega(t_chat_id, part)
            do_rozetka(t_chat_id, row[2], 'reboot')
            sql_string2 = 'UPDATE hive2 ' \
                        'SET time = ? , rig_status = "rebooted" ' \
                        'WHERE rozetka_exists = True and rig_status = "probably" and ' \
                        'rig_online = False and chat_id = ? and rig_id = ? '
            sqz(sql_string2, (timenow, t_chat_id, row[3]))


def re_problems(t_chat_id):
    timenow = dtime.now()
    sql_string = 'SELECT rig_name, rozetka_id, rig_id ' \
                 'FROM hive2 ' \
                 'WHERE rozetka_exists = True and ' \
                 'has_problems = True and rig_online = True and chat_id = ? and is_watchdog = True'
    rows = sqz(sql_string, (t_chat_id,))
    for row in rows:
        part = f'♻️ {row[0]}: есть проблемы — перезагружаем...'
        do_telega(t_chat_id, part)
        do_rozetka(t_chat_id, row[1], 'reboot')
        sql_string_2 = 'UPDATE hive2 ' \
                       'SET time = ? , rig_status = "rebooted", has_problems = False ' \
                       'WHERE rozetka_exists = True and chat_id = ? and rig_id = ? '
        sqz(sql_string_2, (timenow, t_chat_id, row[2]))


def do_emergency(t_chat_id):
    timenow = dtime.now()
    sql_string = 'SELECT time, rig_name, rozetka_id, rig_id ' \
                 'FROM hive2 ' \
                 'WHERE rozetka_exists = True and ' \
                 'rig_status = "rebooted"  and rig_online = False and chat_id = ? and is_watchdog = True'
    rows = sqz(sql_string, (t_chat_id,))
    for row in rows:
        diff = timenow - dtime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
        print('time to shutdown:', diff.seconds)
        if diff.seconds > 600:
            part = f'🆘️ {row[1]}: Авария!!! Риг не перезагрузился за 10 минут, отключаю питание, приезжайте разбирайтесь!'
            do_telega(t_chat_id, part)
            do_rozetka(t_chat_id, row[2], 'off')
            sql_string_2 = 'UPDATE hive2 ' \
                           'SET time = ? , rig_status = "emergency" ' \
                           'WHERE rozetka_exists = True and rig_status = "rebooted"  and ' \
                           'rig_online = False and chat_id = ? and rig_id = ? '
            sqz(sql_string_2, (timenow, t_chat_id, row[3]))


def unemergency(t_chat_id):
    sql_string1 = 'SELECT rozetka_id, rig_name ' \
                  'FROM hive2 ' \
                  'WHERE rozetka_exists = True and ' \
                  'rig_status = "emergency" and rig_online = False and chat_id = ? and is_watchdog = True'
    rows = sqz(sql_string1, (t_chat_id,))
    for row in rows:
        do_telega(t_chat_id, f'🐣 {row[1]}: Пытаюсь восстановить из аварийных')
        do_rozetka(t_chat_id, row[0], 'reboot')
