from modules.connect_sql import sql_zapros as sqz


def add_notify(rig_id, notification_type):
    sql_string = 'INSERT OR IGNORE INTO notify_pool VALUES (?,?)'
    sqz(sql_string, (rig_id, notification_type))
    


def notify_constructor():
    send_text = ''
    sql_string = 'SELECT status_id, status_text ' \
                 'FROM comparison'
    sql_string2 = 'SELECT rig_id ' \
                'FROM notify_pool ' \
                'WHERE notify_id = ? '
    statuses = sqz(sql_string, ())
    for row_status in statuses:
        rig_statuses = sqz(sql_string2, (row_status[0],))
        if len(rig_statuses) != 0:
            send_text = f'{send_text}{row_status[1]}:\n'
            for rig_status in rig_statuses:
                send_text = f'{send_text}    {rig_status[0]}\n'
    print(send_text)