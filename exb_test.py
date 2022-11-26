import modules.exbitron as exb
from  modules.settings import exb_access_key, exb_secret_key

client = exb.Client(access_key = exb_access_key, secret_key = exb_secret_key)
rxd = client.get("/api/v2/peatio/account/balances/rxd")
print(client.check_auth())
print(rxd)


#rxd = usdt = round(float(client.get("/api/v2/peatio/account/balances/rxd")['balance']),2)
#usdt = round(float(client.get("/api/v2/peatio/account/balances/usdt")['balance']),2)
#kas = round(float(client.get("/api/v2/peatio/account/balances/kas")['balance']),2)

