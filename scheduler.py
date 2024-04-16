import time
from main import *

IDLE = 0
MIXER_1 = 1
MIXER_2 = 2
MIXER_3 = 3
PUMP_IN = 4
PUMP_OUT = 5
SELECTOR = 6
NEXT_CYCLE = 7

state = IDLE
next_state=IDLE

time_out = 0

def set_timeout(value):
    global time_out
    time_out=value

set_timeout(5)

while True:
    setDevice1(True,2)
    print("state:" + str(state) + " " + "time: " + str(time_out))
    if (state==IDLE):
        time_out = time_out -1
        if (time_out<=0) :
            print("MIXER 1: ")
            setDevice1(True,2)
            next_state=MIXER_1
            set_timeout(5)
    # elif (state==MIXER_1):
    #     time_out = time_out -1
    #     if (time_out<=0) :
    #         next_state=MIXER_2
    #         set_timeout(5)
    # elif (state==MIXER_2):
    #     time_out = time_out -1
    #     if (time_out<=0) :
    #         next_state=MIXER_3
    #         set_timeout(5)
    # elif (state==MIXER_3):
    #     time_out = time_out -1
    #     if (time_out<=0) :
    #         next_state=PUMP_IN
    #         set_timeout(5)
    # elif (state==PUMP_IN):
    #     time_out = time_out -1
    #     if (time_out<=0) :
    #         next_state=SELECTOR
    #         set_timeout(5)
    # elif (state==SELECTOR):
    #     time_out = time_out -1
    #     if (time_out<=0) :
    #         next_state=PUMP_OUT
    #         set_timeout(5)
    # elif (state==PUMP_OUT):
    #     time_out = time_out -1
    #     if (time_out<=0) :
    #         next_state=NEXT_CYCLE
    #         set_timeout(5)
    # elif (state==NEXT_CYCLE):
    #     time_out = time_out -1
    #     if (time_out<=0) :
    #         next_state=IDLE
    #         set_timeout(5)
    # state=next_state
    time.sleep(1)
    

    