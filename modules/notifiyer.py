from modules.connect_sql import sql_zapros as sqz


def add_notify(rig_id, notification_type):
    sql_string = 'INSERT OR IGNORE INTO notify VALUES (?,?)'
    sqz(sql_string, (rig_id, notification_type))
    


def notify_constructor():
    sql_string = 'SELECT rif_id, notify_id' \
                 'FROM notify_pool'
    rows = sqz(sql_string, ())