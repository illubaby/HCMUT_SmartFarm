import sys
import time
import random
from Adafruit_IO import MQTTClient
start_button = False
MODE = 1
AIO_FEED_ID = ["sonar","current-device", "start-button", "temp", "humid", "mode"]
AIO_USERNAME = "Junnn123"
# AIO_KEY = "aio_GyDq32vQtPzfCEihUi2VYQ3v3da"

def isStart():
    return start_button

def set_start_button(value):
    global start_button
    start_button = value

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Da gui: " + payload + ", feed id: " + feed_id)
    if (feed_id == "start-button"):
        if (payload == "1"):
            global start_button
            start_button = True
            print("ON ada:" + str(start_button))
    elif (feed_id == "mode"):
        global MODE
        if (payload == "1"):
            MODE = 1
        elif (payload == "2"):
            MODE = 2
        elif (payload == "3"):
            MODE = 3

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
