import paho.mqtt.client as paho
import threading
import json
from Modules import PcController

class Subscriber:
    client : paho.Client
    topic: str
    listener_thread: threading.Thread
    callbacks: dict

    def __init__(self, client, topic, callbacks = {}, auto_subscribe = True):
        self.client = client
        self.topic = topic
        self.callbacks = callbacks
        self.listener_thread = threading.Thread(target=client.loop_forever)
        print("Notifier created")

        if auto_subscribe:
            self.subscribe()

    def subscribe(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.subscribe(self.topic)
        print("Subscribed to topic: " + self.topic)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        if rc == 5:
            self.client.disconnect()
            print("Connection refused. Wrong credentials")
            exit(1)

    def register_callback(self, command, callable):
        self.callables[command] = callable

    def listen(self):
        print("Starting listener thread")
        self.listener_thread.start()

    def subscribe_and_listen(self):
        self.subscribe()
        self.listen()
        
    def on_message(self, client, userdata, msg):
        print(f"Message received [{msg.topic}]: {msg.payload}")

        try:
            data = json.loads(msg.payload)
            command = data["command"]
            match command:
                case "callback":
                    if "callback" in data:
                        callback_name = data["callback"]
                    else:
                        callback_name = None

                    if self.callbacks is not None and callback_name is not None and callback_name in self.callbacks:
                        self.callbacks[data["callback"]]()
                    else:
                        print("No callback found for: " + data["callback"])

                case "notify":
                    title = data['title']
                    message = data['msg']

                    PcController.notify(title, message)

                case "lock_pc":
                    PcController.PcController.lock()

                case "sleep_pc":
                    PcController.PcController.sleep()

                case "restart_pc":
                    PcController.PcController.restart()

                case "shutdown_pc":
                    PcController.PcController.shutdown()

                case "hibernate_pc":
                    PcController.PcController.hibernate()
        
        except Exception as e:
            print("Error while parsing message: " + str(e))