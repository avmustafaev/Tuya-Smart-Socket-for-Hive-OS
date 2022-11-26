from datetime import datetime


def start_hour():
    now = datetime.now()
    current_minute = int(now.strftime("%M"))
    current_hour = int(now.strftime("%H"))
    hour_in = current_hour in {7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23}
    minute_in = current_minute >= 0 and current_minute <40
    responce = minute_in and hour_in
    if responce:
        print("Отчёт ключевого часа")
    return responce
