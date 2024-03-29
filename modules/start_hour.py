from datetime import datetime


class StartHour:
    def __init__(self, minutes_window) -> None:
        self.minutes_window = minutes_window

    def start_hour(self):
        now = datetime.now()
        current_minute = int(now.strftime("%M"))
        current_hour = int(now.strftime("%H"))
        #hour_in = current_hour in {9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21}
        hour_in = current_hour in {9}
        minute_in = current_minute >= 0 and current_minute < self.minutes_window
        responce = minute_in and hour_in
        if responce:
            print("Отчёт ключевого часа", current_hour)
        return responce
