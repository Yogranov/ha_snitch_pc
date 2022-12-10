import psutil
from Modules import Entity

DEFAULT_ICON = "mdi:cpu-64-bit"
DEFAULT_UNIT_OF_MEASUREMENT = "%"
DEFAULT_VALUE_TEMPLATE = "{{ value_json.cpu_usage }}"
DEFAULT_ENTITY_TYPE = "sensor"

class CpuUsage(Entity.Entity):
    tolerance : int = 0
    last_state : int = 0

    def __init__(self, client, name, friendly_name, icon = DEFAULT_ICON, tolerance = 5):
        super().__init__(client, name, friendly_name, DEFAULT_ENTITY_TYPE, DEFAULT_UNIT_OF_MEASUREMENT, DEFAULT_VALUE_TEMPLATE, icon)

        self.tolerance = tolerance
        self.state = 0

    def update_state(self):
        self.last_state = self.state
        self.state = psutil.cpu_percent()

    def periodic(self):
        self.update_state()

        should_send_state = abs(self.last_state - self.state) >= self.tolerance
        if should_send_state:
            self.send_state()