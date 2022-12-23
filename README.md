## Main goal of this repo:
The first purpose was to send notification to my pc, and if we already have an active connection, why not send some telemetry data about the pc to home assistant?
But I didn't like the idea of sending data to home assistant every X seconds, so I decided to send data only when needed, and this is the main goal of this repo.

## What is this repo about?
This repo is all about sending a telemetry data about pc to home assistant, and sending commands to pc.
The communication is done via MQTT protocol.

## Big advantage:
The big advantage that I wanted to achieve on this project is the low network traffic, This made by active sending data only after some tolerance changed (~5 by default), so the pc will send data only when needed.


### env_secrets.py (Can be override via config file):
You can create env_secrets.py file and put your secrets there, or you can use the config file.
```python
MQTT_HOST = "192.168.1.1"   # IP of the MQTT broker
MQTT_PORT =  1883           # Port of the MQTT broker
MQTT_USER = "mqtt_user"     # Username of the MQTT broker
MQTT_PASS = "password"      # Password of the MQTT broker