from concurrent.futures import ThreadPoolExecutor
import signal
import threading
from time import sleep
import sys
from libs.devices.driver import uiled as ULED
from libs.devices.driver import buzzer as UIBUZZER 
from libs.devices.driver import uisw as _uisw


def ui_loop(exiting):
    uiled = ULED.UILED()
    uibz = UIBUZZER.buzzer.UIBZ()
    uisw = _uisw.UISW()
    while not exiting.is_set():
        try:
            print("started work 1")
            if uisw.read(uisw.SW0) == True and uisw.read(uisw.SW1) == True and uisw.read(uisw.SW2) == True:
                uiled.write(uiled.UILED0, uiled.UILED_OFF)
                uiled.write(uiled.UILED1, uiled.UILED_OFF)
                uiled.write(uiled.UILED2, uiled.UILED_OFF)
                uiled.write(uiled.UILED3, uiled.UILED_ON)
            elif uisw.read(uisw.SW0) == True and uisw.read(uisw.SW1) == False and uisw.read(uisw.SW2) == False:
                uiled.write(uiled.UILED0, uiled.UILED_ON)
                uiled.write(uiled.UILED1, uiled.UILED_OFF)
                uiled.write(uiled.UILED2, uiled.UILED_OFF)
                uiled.write(uiled.UILED3, uiled.UILED_OFF)
            elif uisw.read(uisw.SW0) == False and uisw.read(uisw.SW1) == True and uisw.read(uisw.SW2) == False:
                uiled.write(uiled.UILED0, uiled.UILED_OFF)
                uiled.write(uiled.UILED1, uiled.UILED_ON)
                uiled.write(uiled.UILED2, uiled.UILED_OFF)
                uiled.write(uiled.UILED3, uiled.UILED_OFF)
            elif uisw.read(uisw.SW0) == False and uisw.read(uisw.SW1) == False and uisw.read(uisw.SW2) == True:
                uiled.write(uiled.UILED0, uiled.UILED_OFF)
                uiled.write(uiled.UILED1, uiled.UILED_OFF)
                uiled.write(uiled.UILED2, uiled.UILED_ON)
                uiled.write(uiled.UILED3, uiled.UILED_OFF)
            else :
                uiled.write(uiled.UILED0, uiled.UILED_OFF)
                uiled.write(uiled.UILED1, uiled.UILED_OFF)
                uiled.write(uiled.UILED2, uiled.UILED_OFF)
                uiled.write(uiled.UILED3, uiled.UILED_OFF)


            uibz.play(freq=440, playLength=0.1)
            uibz.play()

            print("finished work 1")
        except KeyboardInterrupt:
            uiled.close()
            uibz.close()
            uisw.close()
            print("caught keyboardinterrupt")  # never caught here. just for demonstration purposes


def loop_in_worker():
    exiting = threading.Event()
    def signal_handler(signum, frame):
        print("Setting exiting event")
        exiting.set()

    signal.signal(signal.SIGTERM, signal_handler)
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(ui_loop, exiting)

        try:
            while not exiting.is_set():
                sleep(1)
                print('waiting')
        except KeyboardInterrupt:
            print('Caught keyboardinterrupt')
            exiting.set()
    print("Main thread finished (and thus all others)")


if __name__ == '__main__':
    loop_in_worker()
