from modules.connect_sql import sql_zapros as sqz
from modules.get_minute import start_hour
from modules.send_to_telegram import do_telega


def add_notify(rig_id, notification_type):
    sql_string = "INSERT OR IGNORE INTO notify_pool VALUES (?,?)"
    sqz(sql_string, (rig_id, notification_type))


# Разрезалка большого текста для телеграма
def razrez4096(message):
    parts = [""]
    while len(message) > 0:
        if len(message) > 4096:
            partw = message[:4096]
            first_lnbr = partw.rfind("\n")
            if first_lnbr != -1:
                parts.append(partw[:first_lnbr])
                message = message[first_lnbr:]
            else:
                parts.append(partw)
                message = message[4096:]
        else:
            parts.append(message)
            break
    return parts


def notify_constructor():
    send_text = ""
    sql_string = "SELECT status_id, status_text FROM comparison"
    sql_string2 = "SELECT rig_id FROM notify_pool WHERE notify_id = ? "
    statuses = sqz(sql_string, ())
    for row_status in statuses:
        if row_status[0] == "rig_ignored" and start_hour() or row_status[0] != "rig_ignored":
            rig_statuses = sqz(sql_string2, (row_status[0],))
            if len(rig_statuses) != 0:
                send_text = f"{send_text}{row_status[1]}:\n"
                for rig_status in rig_statuses:
                    send_text = f"{send_text}       {rig_status[0]}\n"
    print(send_text)
    partes = razrez4096(send_text)
    for part in partes:
        do_telega(part)
