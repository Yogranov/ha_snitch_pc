from time import sleep
import paho.mqtt.client as paho

from Modules import CameraChecker, Notifier, CpuUsage, MemoryUsage, MicrophoneChecker

import env_secrets

client = paho.Client()
client.username_pw_set(env_secrets.MQTT_USER, env_secrets.MQTT_PASS)
client.connect(env_secrets.MQTT_HOST)

PC_NOTIFICATION_TOPIC = "notify/yogev_pc"
notifier = Notifier.Notifier(client, PC_NOTIFICATION_TOPIC)
notifier.subscribe_and_listen()
print(f"Notifier subscribed to topic: {PC_NOTIFICATION_TOPIC}")

cpu_usage = CpuUsage.CpuUsage(client, "Yogev PC CPU usage", "yogev_pc_cpu_usage")
cpu_usage.send_config()

camera_checker = CameraChecker.CameraChecker(client, "Yogev PC Camera", "yogev_pc_camera")
camera_checker.send_config()

microphone_checker = MicrophoneChecker.MicrophoneChecker(client, "Yogev PC Microphone", "yogev_pc_microphone")
microphone_checker.send_config()

print("Starting main loop")
while True:
    cpu_usage.periodic()
    camera_checker.periodic()
    microphone_checker.periodic()
    sleep(5)

