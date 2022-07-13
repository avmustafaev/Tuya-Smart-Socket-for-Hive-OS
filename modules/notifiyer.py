from modules.connect_sql import sql_zapros as sqz


def add_notify(rig_id, notification_type):
    sql_string = 'INSERT OR IGNORE INTO notify VALUES (?,?)'
    sqz(sql_string, (rig_id, notification_type))