class HiveSync:
    def __init__(self, litecon, os_api, notify, iswatchdog, hive_api) -> None:
        self.osapi = os_api
        self.litecon = litecon
        self.notify = notify
        self.wtchdog = iswatchdog
        self.hiveos_requests_api = hive_api

    def getrig(self):
        rig_response = self.getrigs_api(self.farms_id)
        sql_upd_string = (
            "UPDATE hive2 "
            "SET farm_id=?, rig_name=?, rig_online = ?, is_watchdog = ?, has_problems = ? "
            "WHERE rig_id = ?"
        )
        sql_ins_ignore_str = (
            "INSERT OR IGNORE INTO hive2 VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
        )

        for i in rig_response:
            rig_name = self.del_octothorpe(i.get("name"))  # вернуть октофор
            rig_stats = i.get("stats")
            is_online = rig_stats.get("online")
            is_watchdog_on = self.wtchdog.is_watchdoged(i.get("watchdog"), rig_name)
            has_problems = self.wtchdog.rig_has_problems(
                rig_stats.get("problems"), rig_name
            )
            rig_id = i.get("id")
            cort_upd = (
                self.farms_id,
                rig_name,
                is_online,
                is_watchdog_on,
                has_problems,
                rig_id,
            )
            cort_ins = (
                self.farms_id,
                rig_id,
                rig_name,
                is_online,
                "",
                "working",
                "",
                "",
                is_watchdog_on,
                "",
                "",
                has_problems,
            )
            self.litecon.request(sql_upd_string, cort_upd)
            self.litecon.request(sql_ins_ignore_str, cort_ins)

    def getfarm(self):
        farms_response = self.getfarms_api()
        #print(farms_response)
        sql_string1 = "UPDATE farms_id SET farm_name = ? where farm_id = ?"
        sql_string2 = "INSERT OR IGNORE INTO farms_id VALUES (?,?)"
        for a in farms_response:
            farm_name = a.get("name")
            self.farms_id = str(a.get("id"))
            self.litecon.request(sql_string1, (farm_name, self.farms_id))
            self.litecon.request(sql_string2, (self.farms_id, farm_name))
            self.getrig()

    def del_octothorpe(self, has_octothorpe):
        clean_string = has_octothorpe.replace("#", "")
        if has_octothorpe != clean_string:
            self.notify.add_notify(clean_string, "clean_string")
        return clean_string

    def getfarms_api(self):
        return self.hiveos_requests_api("")["data"]

    def getrigs_api(self, ferms_id):
        return self.hiveos_requests_api(f"{ferms_id}/workers?platform=1&filter=problem")["data"]
