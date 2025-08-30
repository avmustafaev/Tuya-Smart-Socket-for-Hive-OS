""" 
def main():
    envii = Envi()
    hive_api = HiveAPI(envii.hiveos_api)
    telegramer = SendTelega(envii)
    telegramer.do_telega("🚀 Запуск скрипта на сервере.. ")
    starthour = StartHour(envii.minutes_window)
    litecon = LiteConnector()
    notify = Notifyer(
        litecon,
        telegramer,
        starthour,
    )
    checkup = CheckUp(
        litecon.request,
        notify.add_notify,
        telegramer.do_telega,
        envii.pause,
    )
    onoff = WalletPause(
        litecon.request,
        hive_api.hiveos_requests_api,
        telegramer.do_telega,
        starthour.start_hour,
        notify.add_notify,
    )
    
    
    hivesync = HiveSync(
        litecon,
        envii.hiveos_api,
        notify,
        onoff,
        hive_api.hiveos_requests_api,
    )
    tuyaconnector = tinytuya.Cloud(
        envii.tuya_region,
        envii.tuya_api_key,
        envii.tuya_api_secret,
        envii.tuya_device_id,
    )

    mytuya = MyTuya(
        tuyaconnector,
        litecon.request,
    )
    do_switcher = DoSwitch(
        litecon.request,
        tuyaconnector,
    )
    tr = TransferToEmergency(
        envii.hiveos_api,
        litecon.request,
        telegramer.do_telega,
    )
    socket_manager = SocketPoolManager(
        litecon.request,
        do_switcher.do_rozetka,
        tr.transfer,
    )
    hivesync.getfarm()
    mytuya.update_tuya_sockets()
    litecon.backup_db()

    while True:
        if onoff.is_not_pause():
            hivesync.getfarm()
            checkup.go()
            notify.notify_constructor()
            socket_manager.socket_manage()
            litecon.backup_db()
        print(f"Пауза {envii.pause + 10} секунд , до следующей отработки цикла...")
        sleep(envii.pause + 10)


if __name__ == "__main__":
    main() """