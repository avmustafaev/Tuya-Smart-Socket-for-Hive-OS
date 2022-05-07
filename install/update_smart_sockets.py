import sys
sys.path.insert(0, "./")
from modules.hiveosapi import getfarm
from modules.tuya import update_tuya_sockets
from modules.connect_sql import sql_zapros as sqz

sqz('DELETE FROM hive2', ())
sqz('DELETE FROM farms_id', ())

getfarm()
update_tuya_sockets()