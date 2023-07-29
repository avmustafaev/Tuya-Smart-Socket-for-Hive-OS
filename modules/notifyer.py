class Notifyer:
    def __init__(self, connector, telega, start_hour) -> None:
        self.connector = connector
        self.telega = telega
        self.start_hour = start_hour.start_hour

    def add_notify(self, rig_id, notification_type):
        sql_string = "INSERT OR IGNORE INTO notify_pool VALUES (?,?)"
        self.connector.request(sql_string, (rig_id, notification_type))

    def razrez4096(self, message):
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

    def notify_constructor(self):
        send_text = ""
        sql_string = "SELECT status_id, status_text FROM comparison"
        sql_string2 = "SELECT rig_id FROM notify_pool WHERE notify_id = ? "
        statuses = self.connector.request(sql_string, ())
        # очистка уведомлений об игнорируемых ригах
        if not self.start_hour():
            cleared_rig_ids = self.connector.request(sql_string2, ("rig_ignored",))
            sql_del_string = "DELETE FROM notify_pool WHERE rig_id = ? "
            for del_rig in cleared_rig_ids:
                self.connector.request(sql_del_string, (del_rig[0],))
        # конец очистки
        for row_status in statuses:
            if (
                row_status[0] == "rig_ignored"
                and self.start_hour()
                or row_status[0] != "rig_ignored"
            ):
                rig_statuses = self.connector.request(sql_string2, (row_status[0],))
                if len(rig_statuses) != 0:
                    send_text = f"{send_text}{row_status[1]}:\n"
                    for rig_status in rig_statuses:
                        send_text = f"{send_text}       {rig_status[0]}\n"
        print(send_text)
        partes = self.razrez4096(send_text)
        for part in partes:
            self.telega.do_telega(part)
