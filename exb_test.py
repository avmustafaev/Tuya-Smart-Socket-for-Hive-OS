import modules.exbitron as exb

client = exb.Client(access_key = '41be1bdef5d879f9', secret_key = '2a58e1026cbc0be5d838c0886b9275b0')
# rxd = client.get("/api/v2/peatio/account/balances/rxd")
print(client.check_auth())
# print(rxd)


#rxd = usdt = round(float(client.get("/api/v2/peatio/account/balances/rxd")['balance']),2)
#usdt = round(float(client.get("/api/v2/peatio/account/balances/usdt")['balance']),2)
#kas = round(float(client.get("/api/v2/peatio/account/balances/kas")['balance']),2)

