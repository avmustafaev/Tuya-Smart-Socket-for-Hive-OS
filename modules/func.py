import modules.settings as sett
import time
import tinytuya
from modules.connect_sql import sql_zapros as sqz


def select_sw(roz_id):
    sql_string = 'SELECT sw_name FROM hive2 WHERE rozetka_id = ?'
    return sqz(sql_string, (roz_id, ))[0][0]


def do_rozetka(roz_id, doing):
    print(roz_id)
    commands_off = ''
    commands_on = ''
    sw_name = select_sw(roz_id)
    if sw_name == 'switch_1':
        commands_off = {
            'commands': [{
                'code': 'switch_1',
                'value': False
            }, {
                'code': 'countdown_1',
                'value': 0
            }]
        }
        commands_on = {
            'commands': [{
                'code': 'switch_1',
                'value': True
            }, {
                'code': 'countdown_1',
                'value': 0
            }]
        }
    elif sw_name == 'switch':
        commands_off = {
            'commands': [{
                'code': 'switch',
                'value': False
            }, {
                'code': 'countdown_1',
                'value': 0
            }]
        }
        commands_on = {
            'commands': [{
                'code': 'switch',
                'value': True
            }, {
                'code': 'countdown_1',
                'value': 0
            }]
        }
    c = tinytuya.Cloud(sett.tuya_region,
                       sett.tuya_api_key,
                       sett.tuya_api_secret,
                       roz_id)
    
    if doing == 'reboot':
        result = c.sendcommand(roz_id, commands_off)
        print(doing, result)
        time.sleep(20)
        result = c.sendcommand(roz_id, commands_on)
        print(doing, result)
        
    if doing == 'off':
        result = c.sendcommand(roz_id, commands_off)
        print(doing, result)
        
    if doing == 'on':
        result = c.sendcommand(roz_id, commands_on)
        print(doing, result)
