import tinytuya
from connect_sql import sql_zapros as sqz
import settings as sett

device_status = ''
device_id = ''
device_key = ''
device_name = ''

"""Модуль необходимо запускать вручную при добавлении новых розеток или новых ригов

В цикле скачиваются все розетки с облака Tuya и сразу сопоставляются с именами ригов

!!! Модуль запускается после отработки модуля hiveosapi.py

"""

c = tinytuya.Cloud(sett.tuya_region, 
                   sett.tuya_api_key,
                   sett.tuya_api_secret, 
                   sett.tuya_device_id)
devices = c.getdevices()

for i in devices:
    device_name = i.get('name')
    device_id = i.get('id')
    device_key = i.get('key')
    sw_name = ''
    print(device_name)
    print(device_id)
    print(device_key)
    result = c.getstatus(device_id)
    rezul = result['result']
    for x in rezul:
        name = x.get('code')
        val = x.get('value')
        # print(f'▪️  {str(name)} {str(val)}')
        # print(type(val))
        if name in ['switch_1', 'switch']:
            print(f'🚫 {str(name)} {str(val)}')
            sw_name = name
    tu = (sw_name, device_status, device_id, device_key, device_name)
    # print(device_status)
    sql_string1 = 'UPDATE hive2 ' \
                  'SET sw_name = ?, rozetka_status = ?, rozetka_id = ?, ' \
                  'rozetka_key = ?, rozetka_exists = True where rig_name = ? '
    sqz(sql_string1, tu)
    print(' ')
