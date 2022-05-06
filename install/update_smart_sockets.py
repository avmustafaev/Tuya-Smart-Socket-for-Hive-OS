import sys
sys.path.insert(0, "./")
from modules.hiveosapi import getfarm
from modules.tuya import update_tuya_sockets

getfarm()
update_tuya_sockets()