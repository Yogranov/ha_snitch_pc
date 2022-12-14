from time import sleep
import paho.mqtt.client as paho
from Modules import CameraChecker, MicrophoneChecker, CpuUsage, MemoryUsage, MicrophoneChecker, Notifier, GpuTemperature, GpuUsage
import env_secrets

PC_NOTIFICATION_TOPIC = "notify/yogev_pc"
REPUBLISH_CONFIG_TOPIC = "general/republish_config"

# Create a client instance
client = paho.Client()
client.username_pw_set(env_secrets.MQTT_USER, env_secrets.MQTT_PASS)
client.connect(env_secrets.MQTT_HOST)

# Create sensors
camera_checker = CameraChecker.CameraChecker(client)
microphone_checker = MicrophoneChecker.MicrophoneChecker(client)
cpu_usage = CpuUsage.CpuUsage(client)
memory_usage = MemoryUsage.MemoryUsage(client)
gpu_temperature = GpuTemperature.GpuTemperature(client)
gpu_usage = GpuUsage.GpuUsage(client)


# Publish config
camera_checker.send_config()
microphone_checker.send_config()
cpu_usage.send_config()
memory_usage.send_config()
gpu_temperature.send_config()
gpu_usage.send_config()
    

# Subscribers
notifier = Notifier.Notifier(client, PC_NOTIFICATION_TOPIC)
print(f"Notifier subscribed to topic: {PC_NOTIFICATION_TOPIC}")

print("Starting main loop")
while True:
    cpu_usage.periodic()
    gpu_temperature.periodic()
    camera_checker.periodic()
    microphone_checker.periodic()
    memory_usage.periodic()
    gpu_usage.periodic()

    sleep(10)