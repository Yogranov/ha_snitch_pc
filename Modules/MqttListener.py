import paho.mqtt.client as paho
import threading

class MqttListener:
    client : paho.Client = None
    topic: str = None
    listener_thread: threading.Thread = None
    callable = None

    def __init__(self, client, topic, callback = None, auto_subscribe = False):
        self.client = client
        self.topic = topic
        self.callable = callback

        self.listener_thread = threading.Thread(target=client.loop_forever)
        print("MqttListener created")

        if auto_subscribe:
            self.subscribe()

    def subscribe(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.subscribe(self.topic)
        print("Subscribed to topic: " + self.topic)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Message received [{msg.topic}]: {msg.payload}")

        if self.callable is not None:
            self.callable()

    def listen(self):
        print("Starting listener thread")
        self.listener_thread.start()

    def subscribe_and_listen(self):
        self.subscribe()
        self.listen()