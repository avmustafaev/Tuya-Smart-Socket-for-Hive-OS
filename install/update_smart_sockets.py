import sys

from modules.connect_sql import sql_zapros as sqz
from modules.hiveosapi import getfarm
from modules.tuya import update_tuya_sockets

sys.path.insert(0, "./")

sqz("DELETE FROM hive2", ())
sqz("DELETE FROM farms_id", ())

getfarm()
update_tuya_sockets()
