from modules.connect_sql import sql_zapros as sqz

def pauseunpause(value):
    sql_string = 'UPDATE pref SET value = ? where name = ?'
    sqz(sql_string, (value, "pause" ))