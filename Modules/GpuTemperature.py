import GPUtil
from Modules import Entity

DEFAULT_ICON = "mdi:coolant-temperature"
DEFAULT_UNIT_OF_MEASUREMENT = "ºC"
DEFAULT_VALUE_TEMPLATE = "{{ value_json.gpu_temperature }}"
DEFAULT_ENTITY_TYPE = "sensor"

class GpuTemperature(Entity.Entity):
    def __init__(self, client, name, friendly_name, icon = DEFAULT_ICON, tolerance = 5):
        super().__init__(client, name, friendly_name, DEFAULT_ENTITY_TYPE, DEFAULT_UNIT_OF_MEASUREMENT, DEFAULT_VALUE_TEMPLATE, icon, tolerance)

    def update_state(self):
        self.state = GPUtil.getGPUs()[0].temperature