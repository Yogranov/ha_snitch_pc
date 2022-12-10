import psutil
from Modules import Entity

DEFAULT_ICON = "mdi:cpu-64-bit"
DEFAULT_UNIT_OF_MEASUREMENT = "%"
DEFAULT_VALUE_TEMPLATE = "{{ value_json.cpu_usage }}"
DEFAULT_ENTITY_TYPE = "sensor"

class CpuUsage(Entity.Entity):
    def __init__(self, client, name, friendly_name, icon = DEFAULT_ICON):
        super().__init__(client, name, friendly_name, DEFAULT_ENTITY_TYPE, DEFAULT_UNIT_OF_MEASUREMENT, DEFAULT_VALUE_TEMPLATE, icon)

    def update_state(self):
        self.state = psutil.cpu_percent()

    def update_and_send_state(self):
        self.update_state()
        self.send_state()