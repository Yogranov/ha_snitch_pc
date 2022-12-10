
import paho.mqtt.client as paho
import json

DEFAULT_TOPIC = "homeassistant/"

class Entity:
    client : paho.Client
    friendly_name: str
    id: str
    entity_type: str
    unit_of_measurement: str
    value_template: str
    icon: str
    config_topic: str
    state_topic: str

    state = None

    def __init__(self, client, friendly_name, id, entity_type, unit_of_measurement, value_template, icon):
        self.client = client
        self.friendly_name = friendly_name
        self.id = id
        self.entity_type = entity_type
        self.unit_of_measurement = unit_of_measurement
        self.value_template = value_template
        self.icon = icon

        self.config_topic = DEFAULT_TOPIC + self.entity_type + "/" + self.id + "/config"
        self.state_topic = DEFAULT_TOPIC + self.entity_type + "/" + self.id + "/state"

    def send_config(self):
        payload = '{"state_class": "measurement", "name": "' + self.friendly_name + '", "state_topic": "' + self.state_topic + '", "unit_of_measurement": "' + self.unit_of_measurement + '", "value_template": "' + self.value_template + '", "icon": "' + self.icon + '" }'
        self.client.publish(self.config_topic, payload)

    def send_state(self):
        key = self.value_template.split("{{ value_json.")[1][:-2]
        payload = {key: self.state }
        self.client.publish(self.state_topic, json.dumps(payload))

    def update_and_send_state(self, state):
        self.state = state
        self.send_state(state)    
     