class Notifyer:
    def __init__(self, connector, telega, start_hour):
        self.connector = connector
        self.telega = telega
        self.start_hour = start_hour  # Исправлено: сохраняем значение напрямую

    def add_notify(self, rig_id, notification_type):
        sql_string = "INSERT OR IGNORE INTO notify_pool VALUES (?,?)"
        self.connector.request(sql_string, (rig_id, notification_type))

    def split_message(self, message, max_length=4096):
        """Разбивает сообщение на части до max_length, учитывая переводы строк."""
        parts = []
        while len(message) > max_length:
            # Находим последний перевод строки в пределах max_length
            split_pos = message.rfind('\n', 0, max_length)
            if split_pos == -1:
                split_pos = max_length  # Если нет перевода строки, разделяем по длине
            parts.append(message[:split_pos])
            message = message[split_pos:]  # Остальная часть сообщения
        parts.append(message)
        return parts

    def notify_constructor(self):
        send_text = ""
        sql_string = "SELECT status_id, status_text FROM comparison"
        sql_string2 = "SELECT rig_id FROM notify_pool WHERE notify_id = ?"
        
        # Получаем статусы
        statuses = self.connector.request(sql_string, ())
        
        # Очистка уведомлений об игнорируемых ригах
        if not self.start_hour:
            cleared_rig_ids = self.connector.request(sql_string2, ("rig_ignored",))
            delete_query = "DELETE FROM notify_pool WHERE rig_id = ?"
            for rig_id in cleared_rig_ids:
                self.connector.request(delete_query, (rig_id[0],))
        
        # Формируем текст уведомления
        for row_status in statuses:
            if row_status[0] == "rig_ignored":
                if self.start_hour:
                    rig_statuses = self.connector.request(sql_string2, (row_status[0],))
                    if rig_statuses:
                        send_text += f"{row_status[1]}:\n"
                        for rig_status in rig_statuses:
                            send_text += f"       {rig_status[0]}\n"
            else:
                rig_statuses = self.connector.request(sql_string2, (row_status[0],))
                if rig_statuses:
                    send_text += f"{row_status[1]}:\n"
                    for rig_status in rig_statuses:
                        send_text += f"       {rig_status[0]}\n"
        
        # Разбиваем и отправляем сообщение
        message_parts = self.split_message(send_text)
        for part in message_parts:
            self.telega.do_telega(part)
