from datetime import datetime as dtime


class CheckUp:
    def __init__(
        self,
        sqlconnector,
        notifyer,
        telega,
        envpause,
    ) -> None:
        self.sqlreq = sqlconnector
        self.add_notify = notifyer
        self.do_tlgrm = telega
        self.pause = envpause
        self.pause_on = False

    def _execute_sql(self, query: str, params: tuple = None):
        """Универсальный метод для выполнения SQL-запросов"""
        if params is None:
            params = ()
        return self.sqlreq(query, params)

    def _update_rigs_status(
        self, 
        status_condition: str, 
        new_status: str, 
        notification_type: str,
        update_values: dict = None
    ):
        """
        Обновляет статус устройств в БД и отправляет уведомления
        Args:
            status_condition: Условие для выборки устройств
            new_status: Новый статус
            notification_type: Тип уведомления
            update_values: Дополнительные поля для обновления
        """
        select_query = f"""
            SELECT rig_name, rig_id 
            FROM hive2 
            WHERE {status_condition}
        """
        rows = self._execute_sql(select_query)
        
        for row in rows:
            self.add_notify(row[0], notification_type)
            
        update_query = f"""
            UPDATE hive2 
            SET rig_status = '{new_status}'
            {', '.join(f"{k} = ?" for k in update_values or [])}
            WHERE rig_id = ?
        """
        for row in rows:
            params = list(update_values.values()) + [row[1]] if update_values else [row[1]]
            self._execute_sql(update_query, params)

    def _check_time_threshold(
        self,
        time_condition: str,
        threshold_seconds: int,
        action_callback,
        **kwargs
    ):
        """
        Проверяет временные пороги и выполняет действия
        Args:
            time_condition: Условие для выборки по времени
            threshold_seconds: Пороговое значение в секундах
            action_callback: Функция для выполнения при превышении порога
        """
        select_query = f"""
            SELECT time, rig_name, rig_id 
            FROM hive2 
            WHERE {time_condition}
        """
        rows = self._execute_sql(select_query)
        
        for row in rows:
            if self.pause_on:
                self.do_tlgrm("⏸ Поставлен на паузу!")
                break
                
            diff = dtime.now() - dtime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
            if diff.seconds > threshold_seconds:
                action_callback(row[1], row[2], **kwargs)

    def _wakeuped(self):
        """Обработка устройств, которые вернулись к работе"""
        self._update_rigs_status(
            status_condition='rig_status != "working" AND rig_online = True',
            new_status="working",
            notification_type="self_heal",
            update_values={"time": None}
        )

    def _probably_sleeping(self):
        """Обработка устройств, которые, возможно, спят"""
        self._update_rigs_status(
            status_condition='rozetka_exists = True AND rig_status = "working" AND rig_online = False AND is_watchdog = True',
            new_status="probably",
            notification_type="silent",
            update_values={"time": dtime.now()}
        )

    def _bez_rozetki(self):
        """Обработка устройств без розетки"""
        timenow = dtime.now()
        self._update_rigs_status(
            status_condition='rozetka_exists != True AND rig_status = "working" AND rig_online = False',
            new_status="emergency",
            notification_type="no_socket",
            update_values={"time": timenow}
        )

    def _rebooting(self):
        """Обработка устройств, требующих перезагрузки"""
        def handle_reboot(rig_name, rig_id):
            self.add_notify(rig_name, "too_long_silent_reboot")
            self._update_rigs_status(
                status_condition=f'rozetka_exists = True AND rig_status = "probably" AND rig_online = False AND rig_id = {rig_id}',
                new_status="rebooted",
                notification_type=None,
                update_values={"time": dtime.now()}
            )
            
        self._check_time_threshold(
            time_condition='rozetka_exists = True AND rig_status = "probably" AND rig_online = False AND is_watchdog = True',
            threshold_seconds=self.pause,
            action_callback=handle_reboot
        )

    def _re_problems(self):
        """Обработка устройств с проблемами"""
        self._update_rigs_status(
            status_condition='rozetka_exists = True AND has_problems = True AND rig_online = True AND is_watchdog = True',
            new_status="rebooted",
            notification_type="has_problem_reboot",
            update_values={"time": dtime.now(), "has_problems": False}
        )

    def _do_emergency(self):
        """Обработка экстренных ситуаций"""
        def handle_emergency(rig_name, rig_id):
            self.add_notify(rig_name, "is_emergency")
            self._update_rigs_status(
                status_condition=f'rozetka_exists = True AND rig_status = "rebooted" AND rig_online = False AND rig_id = {rig_id}',
                new_status="emergency",
                notification_type=None,
                update_values={"time": dtime.now()}
            )
            
        self._check_time_threshold(
            time_condition='rozetka_exists = True AND rig_status = "rebooted" AND rig_online = False AND is_watchdog = True',
            threshold_seconds=self.pause,
            action_callback=handle_emergency
        )

    def _unemergency(self):
        """Попытка восстановления из экстренной ситуации"""
        select_query = """
            SELECT rozetka_id, rig_name 
            FROM hive2 
            WHERE rozetka_exists = True 
              AND rig_status = "emergency" 
              AND rig_online = False 
              AND is_watchdog = True
        """
        rows = self._execute_sql(select_query)
        print("unemergency:: ", rows)
        
        for row in rows:
            if self.pause_on:
                self.do_tlgrm("⏸ Поставлен на паузу!")
                break
            self.add_notify(row[1], "heal_try")

    def go(self):
        """Основной метод проверки состояния устройств"""
        self._unemergency()
        self._wakeuped()
        self._probably_sleeping()
        self._rebooting()
        self._re_problems()
        self._do_emergency()
        self._bez_rozetki()
