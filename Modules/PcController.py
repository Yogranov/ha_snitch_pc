import os
import ctypes
from win11toast import notify

class PcController:
    def __init__(self):
        pass

    def notify(title, msg, duration="short"):
        notify(title, msg, duration)

    def sleep():
        print("Putting PC to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    def restart():
        print("Restarting PC")
        os.system("shutdown /r /t 0")

    def shutdown():
        print("Shutting down PC")
        os.system("shutdown /s /t 0")

    def hibernate():
        print("Hibernating PC")
        os.system("shutdown /h")

    def lock():
        print("Locking PC")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    def logoff():
        print("Logging off PC")
        os.system("shutdown /l")

    def screen_off():
        print("Turning off screen")
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)

    def screen_on():
        print("Turning on screen")
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, -1)