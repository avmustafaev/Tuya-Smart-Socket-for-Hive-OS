import modules.exbitron
from modules.settings import exb_access_key, exb_secret_key


def get_exbitron():
    client = modules.exbitron.Client(access_key = exb_access_key, secret_key = exb_secret_key)
    rxd = round(float(client.get("/api/v2/peatio/account/balances/rxd")['balance']),2)
    usdt = round(float(client.get("/api/v2/peatio/account/balances/usdt")['balance']),2)
    return f'☢️ Баланс RXD на бирже: {rxd}\n💰 Баланс USDT: {usdt}\n\n🌟\n\n\n'