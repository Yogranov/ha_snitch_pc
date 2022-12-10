from time import sleep
import paho.mqtt.client as paho

from Modules import Notifier, CpuUsage

import env_secrets

client = paho.Client()
client.username_pw_set(env_secrets.MQTT_USER, env_secrets.MQTT_PASS)
client.connect(env_secrets.MQTT_HOST)

PC_NOTIFICATION_TOPIC = "notify/yogev_pc"
notifier = Notifier.Notifier(client, PC_NOTIFICATION_TOPIC)
notifier.subscribe_and_listen()

cpu_usage = CpuUsage.CpuUsage(client, "Yogev PC CPU usage", "yogev_pc_cpu_usage")
cpu_usage.send_config()


while True:
    cpu_usage.update_and_send_state()
    sleep(1)