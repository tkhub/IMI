import threading
from queue import Queue
from time import sleep
from IMI.libs.devices.driver import uiled as UILED
from IMI.libs.devices.driver import uisw as UISW
from IMI.libs.app 

queue_man2machine = Queue()
queue_machine2man = Queue()
queue_sensor = Queue()
killFlag:bool = False

def sensor_loop():
    global killFlag
    print(f"sensor loop = {threading.Thread.name}")
    cnt = 0
    while not killFlag:
        queue_sensor.put(cnt)
        cnt = cnt + 1
        sleep(0.1)

# def run_loop():
#     global killFlag
#     print(f"run loop = {threading.Thread.name}")

#     while not killFlag:
#         if not queue_machine2man.empty():
#             uisws = queue_man2machine.get()

        

def ui_loop():
    global killFlag
    uisw = UISW.UISW()
    uiled = UILED.UILED()
    uisws = (False, False, False)
    uisws_old:tuple[bool, bool, bool] = (False, False, False)
    print(f"ui loop = {threading.Thread.name}")
    while True:
        uisws = (uisw.read(uisw.SW0), uisw.read(uisw.SW1), uisw.read(uisw.SW2))
        if uisws_old != uisws:
            queue_man2machine.put(uisws)
        uisws_old = uisws
        print(f"main loop cnt = {queue_sensor.get()}")
        sleep(0.5)
        if  uisws == (True, True, True):
            print("END")
            killFlag = True
            break
    sleep(1)
    uisw.close()
    uiled.close()

def main():
    print(f"main = {threading.Thread.name}")
    uiThread = threading.Thread(target=ui_loop, daemon=True)
    sensorThread = threading.Thread(target=sensor_loop, daemon=True)
    sensorThread.start()
    uiThread.start()
    uiThread.join()
    sensorThread.join()

if __name__ == "__main__":
    main()