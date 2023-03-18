import psutil
from Modules import Entity

DEFAULT_NAME = "drive_free_storage"
DEFAULT_FRIENDLY_NAME = DEFAULT_NAME.replace("_", " ").title()
DEFAULT_ICON = "mdi:sd"
DEFAULT_UNIT_OF_MEASUREMENT = "GB"
DEFAULT_VALUE_TEMPLATE = "{{ value_json.drive_storage_free }}"
DEFAULT_ENTITY_TYPE = "sensor"

class DriveFreeStorage(Entity.Entity):

    def create_drive_entity(client):
        instances = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            letter = partition.mountpoint[0]
            friendly_name = DEFAULT_FRIENDLY_NAME + " " + letter
            instance = DriveFreeStorage(client, letter, friendly_name)
            instances.append(instance)

        return instances
            


    def __init__(self, client, drive_letter = "C:\\", friendly_name = DEFAULT_FRIENDLY_NAME, icon = DEFAULT_ICON, tolerance = 5):
        self.name = DEFAULT_NAME + "_" + drive_letter
        super().__init__(client, friendly_name, DEFAULT_ENTITY_TYPE, DEFAULT_UNIT_OF_MEASUREMENT, DEFAULT_VALUE_TEMPLATE, icon, tolerance)

    def update_state(self):
        partitions = psutil.disk_partitions()
        for partition in partitions:
            if partition.mountpoint[0] == self.name[-1]:
                free_storage = psutil.disk_usage(partition.mountpoint).free / (1024*1024*1024)
                self.state = round(free_storage, 1)
                break