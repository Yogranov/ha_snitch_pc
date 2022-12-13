from time import sleep
import paho.mqtt.client as paho

from Modules import CameraChecker, MicrophoneChecker, CpuUsage, MemoryUsage, MicrophoneChecker, Notifier, GpuTemperature, GpuUsage

import env_secrets

client = paho.Client()
client.username_pw_set(env_secrets.MQTT_USER, env_secrets.MQTT_PASS)
client.connect(env_secrets.MQTT_HOST)

PC_NOTIFICATION_TOPIC = "notify/yogev_pc"
notifier = Notifier.Notifier(client, PC_NOTIFICATION_TOPIC)
notifier.subscribe_and_listen()
print(f"Notifier subscribed to topic: {PC_NOTIFICATION_TOPIC}")


camera_checker = CameraChecker.CameraChecker(client, "Yogev PC Camera", "yogev_pc_camera")
camera_checker.send_config()

microphone_checker = MicrophoneChecker.MicrophoneChecker(client, "Yogev PC Microphone", "yogev_pc_microphone")
microphone_checker.send_config()

cpu_usage = CpuUsage.CpuUsage(client, "Yogev PC CPU usage", "yogev_pc_cpu_usage")
cpu_usage.send_config()

memory_usage = MemoryUsage.MemoryUsage(client, "Yogev PC Memory usage", "yogev_pc_memory_usage")
memory_usage.send_config()

gpu_temperature = GpuTemperature.GpuTemperature(client, "Yogev PC GPU temperature", "yogev_pc_gpu_temperature")
gpu_temperature.send_config()

gpu_usage = GpuUsage.GpuUsage(client, "Yogev PC GPU usage", "yogev_pc_gpu_usage")
gpu_usage.send_config()



print("Starting main loop")
while True:
    cpu_usage.periodic()
    gpu_temperature.periodic()
    camera_checker.periodic()
    microphone_checker.periodic()
    memory_usage.periodic()
    gpu_usage.periodic()

    sleep(5)

