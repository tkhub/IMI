from concurrent.futures import ThreadPoolExecutor
import signal
import threading
from queue import Queue
from time import sleep, clock_gettime

from IMI.uisystem import UiSystem
from IMI.libs.devices.key import key as UIKey

queue_man2machine = Queue()

# センサ取得。センサからの値を取得して伝える。
def sensorLoop(exiting):
    cnt = 0
    while not exiting.is_set():
        try:
            print(f"{clock_gettime(0)}: sensor cnt = {cnt}")
            cnt += 1
            sleep(0.1)
        except KeyboardInterrupt:
            print("sensor Loop caught keyboardinterrupt")  # never caught here. just for demonstration purposes


# 走行制御。runCmdLoopからの司令や、sensorLoopからの情報を元に走行制御する
def runCtrlLoop(exiting):
    cnt = 0
    while not exiting.is_set():
        try:
            print(f"{clock_gettime(0)}: run Ctrl cnt = {cnt}")
            cnt += 1
            sleep(0.2)
        except KeyboardInterrupt:
            print("Run Control Loop caught keyboardinterrupt")  # never caught here. just for demonstration purposes

# 走行司令。SensorLoopやUIからの情報を元に何をするか決める
def runCmdLoop(exiting):
    cnt = 0
    while not exiting.is_set():
        try:
            print(f"{clock_gettime(0)}: run Cmd cnt = {cnt}")
            if not queue_man2machine.empty():
                print(f"ui = {queue_man2machine.get_nowait()}")
            cnt += 1
            sleep(0.1)
        except KeyboardInterrupt:
            print("Run Cmd Loop caught keyboardinterrupt")  # never caught here. just for demonstration purposes

# スレッド・プロセスを起床するとともに、UIの制御を行う
def displayLoop(exiting):
    cnt = 0
    while not exiting.is_set():
        try:
            print(f"{clock_gettime(0)}: disp cnt = {cnt}")
            cnt += 1
            sleep(0.5)
        except KeyboardInterrupt:
            print("Display Loop caught keyboardinterrupt")  # never caught here. just for demonstration purposes

# スレッド・プロセスを起床するとともに、UIの制御を行う
def main():
    exiting = threading.Event()
    def signal_handler(signum, frame):
        print("Setting exiting event")
        exiting.set()

    signal.signal(signal.SIGTERM, signal_handler)
    with ThreadPoolExecutor() as executor:
        executor.submit(sensorLoop, exiting)
        executor.submit(runCtrlLoop, exiting)
        executor.submit(runCmdLoop, exiting)
        executor.submit(displayLoop, exiting)

        try:
            uikeys = UIKey.Key()
            while not exiting.is_set():
                keycmd = uikeys.detector()
                if keycmd != UIKey.UISWCmd.NON_SW_EVNT:
                    if keycmd == UIKey.UISWCmd.EXIT_PUSH:
                        print("!!! EXIT !!!")
                        exiting.set()
                    else:
                        print(f"enqueue = {keycmd}")
                        queue_man2machine.put_nowait(keycmd)
                sleep(0.05)
        except KeyboardInterrupt:
            print('Main Loop Caught keyboardinterrupt')
            exiting.set()
        finally:
            uikeys.close()
    print("Main thread finished (and thus all others)")


if __name__ == '__main__':
    main()