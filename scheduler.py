import time
from main import *
import random

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

CURRENT_AREA_SELECTED = 4

state = IDLE
next_state=IDLE

time_out = 0

def set_timeout(value):
    global time_out
    time_out=value

set_timeout(5)

setDevice1(True,2)
while True:
    # setDevice1(True,2)
    print("state:" + str(state) + " " + "time: " + str(time_out))
    if (state==IDLE):
        time_out = time_out - 1

        if (readMoisture() < 50 and readTemperature() > 30):
            pass

        if (time_out<=0) :
            print("MIXER 1: ")
            setDevice1(True, MIXER_1_Relay)

            next_state=MIXER_1
            set_timeout(MIXER_1_TIMEOUT)

    elif (state==MIXER_1):
        time_out = time_out - 1
        if (time_out<=0) :
            setDevice1(False, MIXER_1_Relay)
            setDevice1(True, MIXER_2_Relay)

            next_state=MIXER_2
            set_timeout(MIXER_2_TIMEOUT)

    elif (state==MIXER_2):
        time_out = time_out -1
        if (time_out<=0) :
            setDevice1(False, MIXER_2_Relay)
            setDevice1(True, MIXER_3_Relay)

            next_state=MIXER_3
            set_timeout(MIXER_3_TIMEOUT)
            
    elif (state==MIXER_3):
        time_out = time_out -1
        if (time_out<=0) :
            setDevice1(False, MIXER_3_Relay)
            setDevice1(True, PUMP_IN_Relay)

            next_state=PUMP_IN
            set_timeout(PUMP_IN_TIMEOUT)

    elif (state==PUMP_IN):
        time_out = time_out -1
        if (time_out<=0) :
            setDevice1(False, PUMP_IN_Relay)
            setDevice1(True, SELECTOR_Relay)

            next_state=SELECTOR
            CURRENT_AREA_SELECTED = random.randint(4, 6)
            print("Area being irrigated: " + str(CURRENT_AREA_SELECTED))
            set_timeout(SELECTOR_TIMEOUT)

    elif (state==SELECTOR):
        time_out = time_out -1
        if (time_out<=0) :
            setDevice1(False, SELECTOR_Relay)
            setDevice1(True, PUMP_OUT_Relay)

            next_state=PUMP_OUT
            set_timeout(PUMP_OUT_TIMEOUT)

    elif (state==PUMP_OUT):
        time_out = time_out -1
        if (time_out<=0) :
            setDevice1(False, PUMP_OUT_Relay)
            
            next_state=NEXT_CYCLE
            set_timeout(NEXT_CYCLE_TIMEOUT)

    elif (state==NEXT_CYCLE):
        time_out = time_out -1
        if (time_out<=0) :
            next_state=IDLE
            set_timeout(IDLE_TIME_OUT)
            
    state=next_state
    time.sleep(1)
    

    