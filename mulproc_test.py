from concurrent.futures import ThreadPoolExecutor
import signal
import threading
from time import sleep

def loop_worker(exiting):
    while not exiting.is_set():
        try:
            print("started work")
            sleep(10)
            print("finished work")
        except KeyboardInterrupt:
            print("caught keyboardinterrupt")  # never caught here. just for demonstration purposes


def loop_in_worker():
    exiting = threading.Event()
    def signal_handler(signum, frame):
        print("Setting exiting event")
        exiting.set()

    signal.signal(signal.SIGTERM, signal_handler)
    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.submit(loop_worker, exiting)

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