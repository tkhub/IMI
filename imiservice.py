# Standard Library
from concurrent.futures import ThreadPoolExecutor
import signal
from queue import Queue
import time
from typing import Optional

# Third Party Library

# Third Party Library
from IMI.libs.devices.driver import uiled as UILED
from IMI.libs.devices.driver import uisw as UISW
from IMI.libs.devices.wallsensors import wallsensors as WSNS
from IMI.libs.devices.key import key as UIKEY

queue_man2machine = Queue()
queue_machine2man = Queue()
queue_sensor = Queue()
queue_move = Queue()
killFlag:bool = False

def handler(signum, frame):
    print(f"Signal handler called with signal {signum}.")

def sensor_loop():
    global killFlag

    wallsnss = WSNS.wallsensors()
    # print(f"sensor loop = {threading.Thread.name}")
    wss : tuple[Optional[bool], Optional[bool], Optional[bool], Optional[float], Optional[float], Optional[float]] \
        = (None, None, None, None, None, None)
    while not killFlag:
        wst = wallsnss.read()
        wss = ( time.perf_counter_ns(), \
                wst[0], \
                wst[1], \
                wst[2], \
                wst[3], \
                wst[4], \
                wst[5] 
            )
        queue_sensor.put(wss, block=False)
        time.sleep(0.01)
    wallsnss.close()
    # print(f"sensor loop end = {threading.Thread.name}")

def ui_loop():
    global killFlag
    
    uikey = UIKEY.Key()
    uiled = UILED()
    cnt = 0
    while True:
        keyinput = uikey.detector()
        print(queue_sensor.get())
        # if keyinput != UIKEY.UISWCmd.NON_SW_EVNT:
        print(keyinput)
        time.sleep(0.05)
        if keyinput == UIKEY.UISWCmd.EXIT_PUSH:
            print("END")
            killFlag = True
        if killFlag:
            break

    time.sleep(1)
    uikey.close()
    uiled.close()

def main():
    global killFlag
    UIKey = UIKEY.Key()
    try:
        while True:
            SW = UIKey.detector() 
            if SW != UIKEY.UISWCmd.NON_SW_EVNT:
                print(f"return\t= {SW}")
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Ctrl + C is Input")
    finally:
        UIKey.close()

if __name__ == "__main__":
    main()