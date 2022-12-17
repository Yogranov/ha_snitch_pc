import json
import sys 
import paho.mqtt.client as paho
from time import sleep

from Modules.CameraChecker import CameraChecker
from Modules.CpuUsage import CpuUsage
from Modules.MemoryUsage import MemoryUsage
from Modules.MicrophoneChecker import MicrophoneChecker
from Modules.GpuTemperature import GpuTemperature
from Modules.GpuUsage import GpuUsage
from Modules.Subscriber import Subscriber
import env_secrets

# loading config file
options = {}
with open("config.json") as f:
    options = json.load(f)

PC_NOTIFICATION_TOPIC = options["pc_topic"]

# Create a client instance
client = paho.Client()
client.username_pw_set(env_secrets.MQTT_USER, env_secrets.MQTT_PASS)
client.connect(env_secrets.MQTT_HOST)

# Create sensors
sensors = []
for sensor in options["active_sensors"]:
    sensor_name = options["active_sensors"][sensor]
    if sensor_name:
        print(f"Adding sensor: {sensor}")
        sensor_obj = getattr(sys.modules[__name__], sensor)
        sensors.append(sensor_obj(client))

# Publish config
def publish_config():
    for sensor in sensors:
        sensor.send_config()

# Subscriber
subscriber = Subscriber(client, PC_NOTIFICATION_TOPIC, {"republish_config": publish_config})
print(f"Subscriber subscribed to topic: {PC_NOTIFICATION_TOPIC}")
subscriber.listen()

# Publish config on startup
publish_config()
print("Config published")

print("Starting main loop")
while True:
    for sensor in sensors:
        sensor.periodic()

    sleep(10)