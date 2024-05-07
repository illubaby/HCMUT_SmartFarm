import time
from main import *
import random
from adafruit import *
from adafruit import start_button
IDLE = 0
MIXER_1 = 1
MIXER_2 = 2
MIXER_3 = 3
PUMP_IN = 4
PUMP_OUT = 5
SELECTOR = 6
NEXT_CYCLE = 7

MIXER_1_Relay = 2
MIXER_2_Relay = 2
MIXER_3_Relay = 3
PUMP_IN_Relay = 4
PUMP_OUT_Relay = 2
SELECTOR_Relay = 3
NEXT_CYCLE_Relay = 2

IDLE_TIME_OUT = 5
MIXER_1_TIMEOUT = 5
MIXER_2_TIMEOUT = 5
MIXER_3_TIMEOUT = 5
PUMP_IN_TIMEOUT = 5
PUMP_OUT_TIMEOUT = 5
SELECTOR_TIMEOUT = 5
NEXT_CYCLE_TIMEOUT = 5
CYCLE = 3
CURRENT_AREA_SELECTED = 4

state = IDLE
next_state=IDLE

time_out = 0

def Mode1():
    print("Mode: 1")
    MIXER_1_TIMEOUT = 15
    MIXER_2_TIMEOUT = 10
    MIXER_3_TIMEOUT = 20
    PUMP_IN_TIMEOUT = 3
    PUMP_OUT_TIMEOUT = 10
    SELECTOR_TIMEOUT = 5
    NEXT_CYCLE_TIMEOUT = 5
    CYCLE = 2

def Mode2():
    print("Mode: 2")
    MIXER_1_TIMEOUT = 15
    MIXER_2_TIMEOUT = 10
    MIXER_3_TIMEOUT = 20
    PUMP_IN_TIMEOUT = 3
    PUMP_OUT_TIMEOUT = 10
    SELECTOR_TIMEOUT = 5
    NEXT_CYCLE_TIMEOUT = 5
    CYCLE = 2

def Mode3():
    print("Mode: 3")
    MIXER_1_TIMEOUT = 15
    MIXER_2_TIMEOUT = 10
    MIXER_3_TIMEOUT = 20
    PUMP_IN_TIMEOUT = 3
    PUMP_OUT_TIMEOUT = 10
    SELECTOR_TIMEOUT = 5
    NEXT_CYCLE_TIMEOUT = 5
    CYCLE = 2


def set_timeout(value):
    global time_out
    time_out=value

set_timeout(5)

setDevice1(True,2)
client.publish("current-device", "IDLE")

while True:
    print("state:" + str(state) + " " + "time: " + str(time_out))
    time_out = time_out -1
    if (state==IDLE):
        currentTemp = readTemperature()
        currentMoisture = readMoisture()
        if (currentMoisture < 50 and currentMoisture > 30):
            pass
        if (isStart()):
            print("HAHAHAHA")
            client.publish("humid", currentMoisture)
            client.publish("temp", currentTemp)
            if (isMode() == 1):
                Mode1()
                print("Mode 1")
            elif (isMode() == 2):
                Mode2()
                print("Mode 2")
            elif (isMode() == 3):
                Mode3()
                print("Mode 3")
            setDevice1(True, MIXER_1_Relay)
            client.publish("current-device", "MIXER 1")
            next_state=MIXER_1
            set_timeout(MIXER_1_TIMEOUT)
            set_start_button(False)

    elif (state==MIXER_1):
        if (time_out<=0) :
            setDevice1(False, MIXER_1_Relay)
            setDevice1(True, MIXER_2_Relay)
            client.publish("current-device", "MIXER 2")

            next_state=MIXER_2
            set_timeout(MIXER_2_TIMEOUT)

    elif (state==MIXER_2):
        if (time_out<=0) :
            setDevice1(False, MIXER_2_Relay)
            setDevice1(True, MIXER_3_Relay)
            client.publish("current-device", "MIXER 3")

            next_state=MIXER_3
            set_timeout(MIXER_3_TIMEOUT)
            
    elif (state==MIXER_3):
        if (time_out<=0) :
            setDevice1(False, MIXER_3_Relay)
            setDevice1(True, PUMP_IN_Relay)
            client.publish("current-device", "PUMP IN")

            next_state=PUMP_IN
            set_timeout(PUMP_IN_TIMEOUT)

    elif (state==PUMP_IN):
        currentWater = readSonarSensor()
        if (currentWater < 50):
            pass

        if (time_out<=0) :
            client.publish("sonar", currentWater)

            setDevice1(False, PUMP_IN_Relay)
            setDevice1(True, SELECTOR_Relay)

            next_state=SELECTOR
            CURRENT_AREA_SELECTED = random.randint(4, 6)
            client.publish("current-device", "SELECTOR: " + str(CURRENT_AREA_SELECTED))
            print("Area being irrigated: " + str(CURRENT_AREA_SELECTED))
            set_timeout(SELECTOR_TIMEOUT)

    elif (state==SELECTOR):
        if (time_out<=0) :
            setDevice1(False, SELECTOR_Relay)
            setDevice1(True, PUMP_OUT_Relay)
            client.publish("current-device", "PUMP OUT")

            next_state=PUMP_OUT
            set_timeout(PUMP_OUT_TIMEOUT)

    elif (state==PUMP_OUT):
        time_out = time_out -1
        
        if (readSonarSensor() < 10):
            pass

        if (time_out<=0) :
            setDevice1(False, PUMP_OUT_Relay)
            
            next_state=NEXT_CYCLE
            set_timeout(NEXT_CYCLE_TIMEOUT)

    elif (state==NEXT_CYCLE):
        if (time_out<=0) :
            CYCLE = CYCLE - 1
            next_state=MIXER_1
            set_timeout(MIXER_1_TIMEOUT)
            if (CYCLE <= 0):
                # start_button = False
                next_state=IDLE
                client.publish("current-device", "IDLE")
                client.publish("start-button", 0)
            else:
                setDevice1(True, MIXER_1_Relay)
                client.publish("current-device", "MIXER 1") 

    state=next_state
    
    time.sleep(1)
    

    