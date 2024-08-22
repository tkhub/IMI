from concurrent.futures import ThreadPoolExecutor
import queue
import signal
import threading
from queue import Queue
from time import sleep, clock_gettime, clock_gettime_ns

from IMI import runcontroller
from IMI.runcommander import IMICommander, IMIModeChoice, RunMode
from IMI.uisystem import UiSystem

from IMI.libs.devices.key import key as UIKey
from IMI.libs.devices.sound import sound as UISound
from IMI.libs.devices.wallsensors import wallsensors as Wallsensors

from IMI.imimessage import IMISensorsDict,RunCmd
from IMI.imisensor import IMISensor
from IMI.uisystem import UiSystem
from IMI.runcontroller import RunExecutor

queue_man2machine = Queue()
queue_sensor = Queue(maxsize=1)
queue_cmd2exec = Queue()
queue_exec2cmd = Queue(maxsize=1)

# # センサ取得。センサからの値を取得して伝える。
def sensorLoop(exiting):
    WSensor = IMISensor()
    while not exiting.is_set():
        try:
            if not queue_sensor.full():
                snsvals = WSensor.read(clock_gettime_ns(0))
                queue_sensor.put(snsvals)
            sleep(0.01)
        except KeyboardInterrupt:
            print("sensor Loop caught keyboardinterrupt")  # never caught here. just for demonstration purposes
    WSensor.close()


# 走行制御。runCmdLoopからの司令や、sensorLoopからの情報を元に走行制御する
def runCtrlLoop(exiting):
    cnt = 0
    snsvals:IMISensorsDict
    executor = runcontroller.RunExecutor()
    WSensor = IMISensor()
    while not exiting.is_set():
        try:
            # if not queue_test.empty():
            #     executor.move(200,queue_test.get_nowait())
            # else:
            #     executor.move(200,RunCmd.STOP)
                # sleep(0.01)
            # if not queue_sensor.empty():
            #     tmp = queue_sensor.get()
            # else:
            #     print("Empty")
            # if not queue_cmd2exec.empty():
            #     snsvals = WSensor.read(clock_gettime_ns(0))
            #     executor.move(200, queue_cmd2exec.get(), sensor=snsvals["wallvalue"])
            # print("ctrlloop")
            # sleep(0.1)
                # if queue_exec2cmd.full():
                #     queue_exec2cmd.put(snsvals["wallflag"])
            # if not queue_sensor.empty():
                # snsvals = queue_sensor.get_nowait()
            tmp = WSensor.read(clock_gettime_ns(0))
            tmp2 = tmp["wallflag"] + tmp["wallvalue"]
            executor.move(200, queue_cmd2exec.get())
            sleep(0.01)
        except KeyboardInterrupt:
            print("Run Control Loop caught keyboardinterrupt")  # never caught here. just for demonstration purposes
        WSensor.close()

# 走行司令。SensorLoopやUIからの情報を元に何をするか決める
def runCmdLoop(exiting):
    cnt = 0
    key:UIKey.UISWCmd = UIKey.UISWCmd.NON_SW_EVNT
    mode:RunMode = RunMode.NOP
    while not exiting.is_set():
        try:
            # if not queue_man2machine.empty():
            #     key = queue_man2machine.get()
            #     print(f"key = {key}")
            #     IMIModeChoice(key) 
            # if flag == False:
            #     flag = True
            #     queue_cmd2exec.put(IMICommander(timestamp=clock_gettime_ns(0)))
            # elif not queue_exec2cmd.empty():
            #     queue_cmd2exec.put(IMICommander(timestamp=clock_gettime_ns(0), wallflag=queue_exec2cmd.get()))
            # queue_cmd2exec.put(IMICommander(timestamp=clock_gettime_ns(0)))
            #queue_cmd2exec.put(IMICommander(timestamp=clock_gettime_ns(0), wallflag=queue_exec2cmd.get()))
            if not queue_man2machine.empty():
                key = queue_man2machine.get()
                print(f"key = {key}")
                IMIModeChoice(key) 
            else:
                sleep(0.05)
            queue_cmd2exec.put(IMICommander(timestamp=clock_gettime_ns(0)))
        except KeyboardInterrupt:
            print("Run Cmd Loop caught keyboardinterrupt")  # never caught here. just for demonstration purposes

# スレッド・プロセスを起床するとともに、UIの制御を行う
def displayLoop(exiting):
    cnt = 0
    while not exiting.is_set():
        try:
            pass
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
        executor.submit(runCtrlLoop, exiting)
        executor.submit(runCmdLoop, exiting)
        executor.submit(displayLoop, exiting)

        try:
            uikeys = UIKey.Key()
            uisound = UISound.Sound()
            while not exiting.is_set():
                keycmd = uikeys.detector()
                if keycmd != UIKey.UISWCmd.NON_SW_EVNT:
                    print(keycmd)
                    if keycmd == UIKey.UISWCmd.EXIT_PUSH:
                        print("!!! EXIT !!!")
                        exiting.set()
                        uisound.play(uisound.Pattern.CANCEL_0)
                    else:
                        print(f"UI   PUSH = {keycmd}")
                        queue_man2machine.put(keycmd)
                sleep(0.05)
        except KeyboardInterrupt:
            print('Main Loop Caught keyboardinterrupt')
            exiting.set()
        finally:
            uikeys.close()
            uisound.close()
    print("Main thread finished (and thus all others)")


if __name__ == '__main__':
    main()

    
# ディスプレイで現在のモードを確認する
# モードを選ぶ(SEL ENT ESC)
# 選んだモードで何を行わせるのか決める
# 
# 前に進むとか曲がるとかが行われる

# root 
#  | 
#  +----RUN----+----Search
#  |           |
#  |           +----Fast0
#  |           |
#  |           |----Fast1
#  |           |     :
#  |           :     :
#  |           :     :
#  |           
#  | 
#  +----TEST---+----TURN
#              |
#              +----SENSOR