import GPUtil
from Modules import Entity

DEFAULT_NAME = "gpu_usage"
DEFAULT_FRIENDLY_NAME = DEFAULT_NAME.replace("_", " ").title()
DEFAULT_ICON = "mdi:expansion-card"
DEFAULT_UNIT_OF_MEASUREMENT = "%"
DEFAULT_VALUE_TEMPLATE = "{{ value_json.gpu_usage }}"
DEFAULT_ENTITY_TYPE = "sensor"

class GpuUsage(Entity.Entity):
    def __init__(self, client, friendly_name = DEFAULT_FRIENDLY_NAME, icon = DEFAULT_ICON, tolerance = 5):
        self.name = DEFAULT_NAME
        super().__init__(client, friendly_name, DEFAULT_ENTITY_TYPE, DEFAULT_UNIT_OF_MEASUREMENT, DEFAULT_VALUE_TEMPLATE, icon, tolerance)

    def update_state(self):
        self.state = GPUtil.getGPUs()[0].load * 100