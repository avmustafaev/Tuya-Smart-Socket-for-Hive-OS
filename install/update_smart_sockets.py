import sys

from modules.lite_connector import sql_zapros as sqz
from modules.hive_sync import getfarm
from modules.my_tuya import update_tuya_sockets

sys.path.insert(0, "./")

sqz("DELETE FROM hive2", ())
sqz("DELETE FROM farms_id", ())

getfarm()
update_tuya_sockets()
