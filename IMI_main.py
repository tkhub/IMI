from concurrent.futures import ThreadPoolExecutor
import signal
import threading
from queue import Queue
from time import sleep, clock_gettime

from IMI.libs.devices.key import key as UIKey

queue_man2machine = Queue()

def sensorLoop(exiting):
    cnt = 0
    while not exiting.is_set():
        try:
            print(f"{clock_gettime(0)}: sensor cnt = {cnt}")
            cnt += 1
            sleep(0.1)
        except KeyboardInterrupt:
            print("caught keyboardinterrupt")  # never caught here. just for demonstration purposes

def runCtrlLoop(exiting):
    cnt = 0
    while not exiting.is_set():
        try:
            print(f"{clock_gettime(0)}: run cnt = {cnt}")
            if not queue_man2machine.empty():
                print(f"ui = {queue_man2machine.get_nowait()}")
            cnt += 1
            sleep(0.5)
        except KeyboardInterrupt:
            print("caught keyboardinterrupt")  # never caught here. just for demonstration purposes

def runCmdLoop(exiting):
    cnt = 0
    while not exiting.is_set():
        try:
            print(f"{clock_gettime(0)}: run cnt = {cnt}")
            if not queue_man2machine.empty():
                print(f"ui = {queue_man2machine.get_nowait()}")
            cnt += 1
            sleep(0.5)
        except KeyboardInterrupt:
            print("caught keyboardinterrupt")  # never caught here. just for demonstration purposes

def main():
    exiting = threading.Event()
    def signal_handler(signum, frame):
        print("Setting exiting event")
        exiting.set()

    signal.signal(signal.SIGTERM, signal_handler)
    with ThreadPoolExecutor() as executor:
        executor.submit(runCtrlLoop, exiting)
        executor.submit(sensorLoop, exiting)

        try:
            uikeys = UIKey.Key()
            while not exiting.is_set():
                keycmd = uikeys.detector()
                if keycmd != UIKey.UISWCmd.NON_SW_EVNT:
                    print(f"enqueue = {keycmd}")
                    queue_man2machine.put_nowait(keycmd)
                sleep(0.05)
        except KeyboardInterrupt:
            print('Caught keyboardinterrupt')
            exiting.set()
        finally:
            uikeys.close()
    print("Main thread finished (and thus all others)")


if __name__ == '__main__':
    main()