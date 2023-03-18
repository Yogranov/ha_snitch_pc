import json
from time import sleep
from Modules import PcController
import subprocess

class Subscriber:
    def __init__(self, client, topic, callbacks = {}):
        self.client = client
        self.topic = topic
        self.callbacks = callbacks
        print("Notifier created")
        # Set callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def listen(self):
        print("Listening for messages...")
        self.client.loop_start()

    def register_callback(self, command, callable):
        self.callables[command] = callable
        print("Registered callback for command: " + command)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        if rc == 5:
            self.client.disconnect()
            print("Connection refused. Wrong credentials")
            exit(1)

        self.client.subscribe(self.topic)

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnected with result code {rc}")
        if rc != 0:
            sleep(20)
            self.client.reconnect()
            self.client.subscribe(self.topic)


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

                case "screen_off":
                    PcController.PcController.screen_off()

                case "screen_on":
                    PcController.PcController.screen_on()

                case "update_app":
                    print("Updating app")
                    cmd = r"venv/Scripts/python update.py"
                    subprocess.call(cmd)
                    exit(0)

        
        except Exception as e:
            print("Error while parsing message: " + str(e))