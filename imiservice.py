# Standard Library
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from time import sleep
from typing import Optional

# Third Party Library

# Third Party Library
from IMI.libs.devices.driver import uiled as UILED
from IMI.libs.devices.driver import uisw as UISW
from IMI.libs.devices.wallsensors import wallsensors as WSNS

queue_man2machine = Queue()
queue_machine2man = Queue()
queue_sensor = Queue()
queue_move = Queue()
killFlag:bool = False

def sensor_loop():
    global killFlag

    wallsnss = WSNS.wallsensors()
    # print(f"sensor loop = {threading.Thread.name}")
    wss : tuple[Optional[bool], Optional[bool], Optional[bool], Optional[float], Optional[float], Optional[float]] \
        = (None, None, None, None, None, None)
    while not killFlag:
        wss = wallsnss.read()
        queue_sensor.put(wss)
        sleep(0.01)
    wallsnss.close()
    # print(f"sensor loop end = {threading.Thread.name}")

def ui_loop():
    global killFlag
    uisw = UISW.UISW()
    uiled = UILED.UILED()
    uisws = (False, False, False)
    uisws_old:tuple[bool, bool, bool] = (False, False, False)
    uisws_old2:tuple[bool, bool, bool] = (False, False, False)
    # print(f"ui loop = {threading.Thread.name}")
    while True:
        uisws = (uisw.read(uisw.SW0), uisw.read(uisw.SW1), uisw.read(uisw.SW2))
        if uisws_old != uisws:
            queue_man2machine.put(uisws)
        uisws_old = uisws
        sleep(0.5)
        if  uisws == (True, True, True):
            print("END")
            killFlag = True
            break
    sleep(1)
    uisw.close()
    uiled.close()
    # print(f"ui loop end = {threading.Thread.name}")

def main():
    # print(f"main = {threading.Thread.name}")
    # uiThread = threading.Thread(target=ui_loop, daemon=True)
    # sensorThread = threading.Thread(target=sensor_loop, daemon=True)
    # # runThread = threading.Thread(target=run_loop, daemon=True)
    # uiThread.start()
    # sensorThread.start()
    # # runThread.start()
    # uiThread.join()
    # # runThread.join()
    # sensorThread.join()
    with ThreadPoolExecutor() as executor:
        uiExec = executor.submit(ui_loop)
        sensorExec = executor.submit(sensor_loop)


if __name__ == "__main__":
    main()