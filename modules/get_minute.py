from datetime import datetime


def start_hour():
    now = datetime.now()
    current_minute = int(now.strftime("%M"))
    respone = current_minute >= 0 and current_minute <11
    if respone:
        print("Отчёт начала часа")
    return respone

