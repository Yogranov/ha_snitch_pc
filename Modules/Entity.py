
import paho.mqtt.client as paho
import json
import os

DEFAULT_TOPIC = "homeassistant/"

class Entity:
    client : paho.Client
    friendly_name: str
    name: str
    entity_type: str
    unit_of_measurement: str
    value_template: str
    icon: str
    config_topic: str
    state_topic: str

    state = 0
    last_sent_state = 0
    tolerance : int = 0


    def __init__(self, client, friendly_name, entity_type, unit_of_measurement, value_template, icon, tolerance = 5):
        self.client = client
        self.friendly_name = friendly_name
        self.entity_type = entity_type
        self.unit_of_measurement = unit_of_measurement
        self.value_template = value_template
        self.icon = icon

        self.name = os.getenv('username') + "_" + self.name
        self.tolerance = tolerance
        self.config_topic = DEFAULT_TOPIC + self.entity_type + "/" + self.name + "/config"
        self.state_topic = DEFAULT_TOPIC + self.entity_type + "/" + self.name + "/state"

    def send_config(self):
        payload = '{"name": "' + self.name + '", "state_topic": "' + self.state_topic + '", "unit_of_measurement": "' + self.unit_of_measurement + '", "value_template": "' + self.value_template + '", "icon": "' + self.icon + '" }'
        # payload = '{"state_class": "measurement", "name": "' + self.friendly_name + '", "state_topic": "' + self.state_topic + '", "unit_of_measurement": "' + self.unit_of_measurement + '", "value_template": "' + self.value_template + '", "icon": "' + self.icon + '" }'
        self.client.publish(self.config_topic, payload)
        print(f"Config published to topic: {self.config_topic}")

    def send_state(self):
        # print(f"Sending state: {self.state} to topic: {self.state_topic}")
        key = self.value_template.split("{{ value_json.")[1][:-3]
        payload = {key: self.state }

        # print(f"Payload: {json.dumps(payload)}")
        self.client.publish(self.state_topic, json.dumps(payload))

        self.last_sent_state = self.state

    def update_and_send_state(self, state):
        self.state = state
        self.send_state(state)    
     
    def update_state(self, state):
        # Override this method
        self.state = state

    def periodic(self):
        self.update_state()
        # print(f"State: {self.state}, Last state: {self.last_sent_state}")

        if self.entity_type == "sensor":
            should_send_state = abs(self.last_sent_state - self.state) >= self.tolerance
            # print(f"Should send state: {should_send_state}")
            if should_send_state:
                self.send_state()

        elif self.entity_type == "binary_sensor":
            if self.state == True:
                self.state = "ON"
            elif self.state == False:
                self.state = "OFF"
                
            if self.state != self.last_sent_state:
                self.send_state()

        else:
            print("Entity type not supported")
            return

