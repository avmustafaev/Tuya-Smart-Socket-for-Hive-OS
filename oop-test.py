from modules.loadenvi import Envi
from modules.lite_connector import LiteConnector
from modules.hive_sync import HiveSync
from modules.notifyer import Notifyer
from modules.telega import SendTelega
from modules.start_hour import StartHour
from modules.my_tuya import MyTuya
import tinytuya


envii = Envi()
starthour = StartHour(envii.minutes_window)
telegramer = SendTelega(envii)
litecon = LiteConnector()
notify = Notifyer(litecon, telegramer, starthour)
hivesync = HiveSync(litecon, envii.hiveos_api, notify)
tuyaconnector = tinytuya.Cloud(envii.tuya_region, envii.tuya_api_key, envii.tuya_api_secret,envii.tuya_device_id)
mytuya = MyTuya(tuyaconnector, litecon.request)
litecon.backup_db()






