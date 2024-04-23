import sys
import time
import random
from Adafruit_IO import MQTTClient
AIO_FEED_ID = ["sonar","current-device", "start-button", "temp", "humid"]
AIO_USERNAME = "Junnn123"
# AIO_KEY = "aio_GyDq32vQtPzfCEihUi2VYQ3v3da"

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

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

