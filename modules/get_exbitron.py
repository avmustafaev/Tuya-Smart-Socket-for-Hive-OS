import modules.exbitron as exb
from modules.settings import exb_access_key, exb_secret_key

def get_exbitron():
    client = exb.Client(access_key = exb_access_key, secret_key = exb_secret_key)
    rxd = client.get("/api/v2/peatio/account/balances/rxd")
    usdt = client.get("/api/v2/peatio/account/balances/usdt")
    kas = client.get("/api/v2/peatio/account/balances/kas")
    rxd_balance = round(float(rxd['balance']),2)
    rxd_locked = round(float(rxd['locked']),2)
    usdt_locked = round(float(usdt['locked']),2)
    kas_locked = round(float(kas['locked']),2)
    usdt_balance = round(float(usdt['balance']),2)
    kas_balance = round(float(kas['balance']),2)
    return f'💰💰💰\nUSDT\nbalance: {usdt_balance}\nlocked: {usdt_locked}\n\nRXD\nbalance: {rxd_balance}\nlocked: {rxd_locked}\n\nKAS\nbalance {kas_balance}\nlocked: {kas_locked}\n💰💰💰\n'
