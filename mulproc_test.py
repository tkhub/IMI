from concurrent.futures import ThreadPoolExecutor
import signal
import threading
from time import sleep, clock_gettime
from queue import Queue

testq = Queue(maxsize=1)

def loop_worker1(exiting):
    cnt:int = 0
    while not exiting.is_set():
        try:
            if not testq.full():
                testq.put((clock_gettime(0), cnt))
            else:
                print("full")
            cnt += 1
            sleep(0.1)
        except KeyboardInterrupt:
            print("caught keyboardinterrupt")  # never caught here. just for demonstration purposes

def loop_worker2(exiting):
    while not exiting.is_set():
        try:
            if not testq.empty():
                # print(f"t = {clock_gettime(0)} sensor = {testq.get_nowait()}")
                print(f"t = {clock_gettime(0)} sensor = {testq.get()}")
            else:
                print("empty")
            sleep(0.5)
        except KeyboardInterrupt:
            print("caught keyboardinterrupt")  # never caught here. just for demonstration purposes

def loop_in_worker():
    exiting = threading.Event()
    def signal_handler(signum, frame):
        print("Setting exiting event")
        exiting.set()

    signal.signal(signal.SIGTERM, signal_handler)
    with ThreadPoolExecutor() as executor:
        executor.submit(loop_worker1, exiting)
        executor.submit(loop_worker2, exiting)

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