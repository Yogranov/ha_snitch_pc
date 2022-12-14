import winreg
import os
from Modules import Entity

DEFAULT_NAME = "camera_activate"
DEFAULT_FRIENDLY_NAME = DEFAULT_NAME.replace("_", " ").title()
DEFAULT_ICON = "mdi:camera"
DEFAULT_UNIT_OF_MEASUREMENT = "%"
DEFAULT_VALUE_TEMPLATE = "{{ value_json.is_cam_active }}"
DEFAULT_ENTITY_TYPE = "binary_sensor"

REG_KEY = winreg.HKEY_CURRENT_USER
WEBCAM_REG_SUBKEY = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam\\NonPackaged"
WEBCAM_TIMESTAMP_VALUE_NAME = "LastUsedTimeStop"

class CameraChecker(Entity.Entity):
    def __init__(self, client, friendly_name = DEFAULT_FRIENDLY_NAME, icon = DEFAULT_ICON, tolerance = 5):
        self.name = DEFAULT_NAME
        super().__init__(client, friendly_name, DEFAULT_ENTITY_TYPE, DEFAULT_UNIT_OF_MEASUREMENT, DEFAULT_VALUE_TEMPLATE, icon, tolerance)

    def update_state(self):
        self.state = self.isActive()

    def getActiveApps(self):
        activeApps = []
        regKey = winreg.OpenKey(REG_KEY, WEBCAM_REG_SUBKEY)
        
        subkeyCnt, _, _ = winreg.QueryInfoKey(regKey)
        for idx in range(subkeyCnt):
            subkeyName = winreg.EnumKey(regKey, idx)
            subkeyFullName = f"{WEBCAM_REG_SUBKEY}\\{subkeyName}"
            subkey = winreg.OpenKey(REG_KEY, subkeyFullName)
            stoppedTimestamp, _ = winreg.QueryValueEx(subkey, WEBCAM_TIMESTAMP_VALUE_NAME)

            if 0 == stoppedTimestamp:
                app_name = subkeyName.split("#")[-1].split(".")[0]
                activeApps.append(app_name)

        return activeApps


    def isActive(self):
        return len(self.getActiveApps()) > 0

