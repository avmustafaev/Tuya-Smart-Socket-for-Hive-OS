from datetime import datetime


def start_hour():
    now = datetime.now()
    current_minute = int(now.strftime("%M"))
    current_hour = int(now.strftime("%H"))
    hour_in = current_hour in {8, 12, 15, 17, 20}
    minute_in = current_minute >= 0 and current_minute <11
    responce = minute_in and hour_in
    if responce:
        print("Отчёт ключевого часа")
    return responce
