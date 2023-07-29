import requests


class SendTelega:
    def __init__(self, env) -> None:
        self.tel_api = env.telegram_api
        self.chat_id = env.chat_id

    def do_telega(self, part):
        requests.get(
            f"https://api.telegram.org/bot{self.tel_api}/sendMessage?text={part}&chat_id={self.chat_id}"
        )
