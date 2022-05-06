import sqlite3


def sql_zapros(sql_string, tupple):
    connection = sqlite3.connect('smartsocket.db')
    cursor = connection.cursor()
    cursor.execute(sql_string, tupple)
    response_list = cursor.fetchall()
    connection.commit()
    connection.close()
    return response_list
