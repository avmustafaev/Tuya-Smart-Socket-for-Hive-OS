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

    def _wakeuped(self):
        sql_string = (
            "SELECT rig_status, rig_name "
            "FROM hive2 "
            'WHERE rig_status != "working"  and rig_online = True'
        )
        rows = self.sqlreq(sql_string, ())
        for row in rows:
            if row[0] == "probably":
                self.add_notify(row[1], "self_heal")
            if row[0] == "rebooted":
                self.add_notify(row[1], "socket_healed")
            if row[0] == "emergency":
                self.add_notify(row[1], "heal_from_emergency")
        sql_string2 = (
            "UPDATE hive2 "
            'SET time = NULL , rig_status = "working" '
            'WHERE rig_status != "working"  and rig_online = True'
        )
        self.sqlreq(sql_string2, ())

    def _probably_sleeping(self):
        sql_string1 = (
            "SELECT rig_name "
            "FROM hive2 "
            'WHERE rozetka_exists = True and rig_status = "working"  '
            "and rig_online = False and is_watchdog = True"
        )
        rows = self.sqlreq(sql_string1, ())
        for row in rows:
            self.add_notify(row[0], "silent")
        sql_string2 = (
            "UPDATE hive2 "
            'SET time = ? , rig_status = "probably" '
            'WHERE rozetka_exists = True and rig_status = "working"  and rig_online = False'
        )
        self.sqlreq(sql_string2, (dtime.now(),))

    def _bez_rozetki(self):
        timenow = dtime.now()
        sql_string1 = (
            "SELECT rig_name, rig_id "
            "FROM hive2 "
            'WHERE rozetka_exists != True and rig_status = "working"  and rig_online = False'
        )
        rows = self.sqlreq(sql_string1, ())
        for row in rows:
            self.add_notify(row[0], "no_socket")
            sql_string2 = (
                "UPDATE hive2 "
                'SET time = ? , rig_status = "emergency" '
                "WHERE rig_id = ?"
            )
            self.sqlreq(sql_string2, (timenow, row[1]))

    def _rebooting(self):
        timenow = dtime.now()
        sql_string1 = (
            "SELECT time, rig_name, rozetka_id, rig_id "
            "FROM hive2 "
            'WHERE rozetka_exists = True and rig_status = "probably"  '
            "and rig_online = False and is_watchdog = True"
        )
        rows = self.sqlreq(sql_string1, ())
        for row in rows:
            if self.pause_on:
                self.do_tlgrm("⏸ Поставлен на паузу!")
                break
            diff = timenow - dtime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
            print("time to reboot:", diff.seconds)
            if diff.seconds > self.pause:
                self.add_notify(row[1], "too_long_silent_reboot")
                sql_string2 = (
                    "UPDATE hive2 "
                    'SET time = ? , rig_status = "rebooted" '
                    'WHERE rozetka_exists = True and rig_status = "probably" and '
                    "rig_online = False and rig_id = ? "
                )
                self.sqlreq(sql_string2, (timenow, row[3]))

    def _re_problems(self):
        timenow = dtime.now()
        sql_string = (
            "SELECT rig_name, rozetka_id, rig_id "
            "FROM hive2 "
            "WHERE rozetka_exists = True and "
            "has_problems = True and rig_online = True and is_watchdog = True"
        )
        rows = self.sqlreq(sql_string, ())
        for row in rows:
            if self.pause_on:
                self.do_tlgrm("⏸ Поставлен на паузу!")
                break
            self.add_notify(row[0], "has_problem_reboot")
            sql_string_2 = (
                "UPDATE hive2 "
                'SET time = ? , rig_status = "rebooted", has_problems = False '
                "WHERE rozetka_exists = True and rig_id = ? "
            )
            self.sqlreq(sql_string_2, (timenow, row[2]))

    def _do_emergency(self):
        timenow = dtime.now()
        sql_string = (
            "SELECT time, rig_name, rozetka_id, rig_id "
            "FROM hive2 "
            "WHERE rozetka_exists = True and "
            'rig_status = "rebooted"  and rig_online = False and is_watchdog = True'
        )
        rows = self.sqlreq(sql_string, ())
        for row in rows:
            if self.pause_on:
                self.do_tlgrm("⏸ Поставлен на паузу!")
                break
            diff = timenow - dtime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
            print("time to shutdown:", diff.seconds)
            if diff.seconds > self.pause:
                self.add_notify(row[1], "is_emergency")
                sql_string_2 = (
                    "UPDATE hive2 "
                    'SET time = ? , rig_status = "emergency" '
                    'WHERE rozetka_exists = True and rig_status = "rebooted"  and '
                    "rig_online = False and rig_id = ? "
                )
                self.sqlreq(sql_string_2, (timenow, row[3]))

    def _unemergency(self):
        sql_string1 = (
            "SELECT rozetka_id, rig_name "
            "FROM hive2 "
            "WHERE rozetka_exists = True and "
            'rig_status = "emergency" and rig_online = False and is_watchdog = True'
        )
        rows = self.sqlreq(sql_string1, ())
        print("unemergency:: ", rows)
        for row in rows:
            if self.pause_on:
                self.do_tlgrm("⏸ Поставлен на паузу!")
                break
            self.add_notify(row[1], "heal_try")

    def go(self):
        self._unemergency()
        self._wakeuped()
        self._probably_sleeping()
        self._rebooting()
        self._re_problems()
        self._do_emergency()
        self._bez_rozetki()
