import threading
import multiprocessing
from time import sleep, clock_gettime_ns
import signal
import sys
import os
from threading import Thread, Event
from multiprocessing import Process, Manager, Queue


import pigpio

from IMI.imimessage import JOB, ExecJob, RunCmd, SoundPattern, JOB_STATE
from IMI.runcommander import commandSetter
from IMI.uisystem import JobControler, Sound
from IMI.libs.devices.wallsensors.wallsensors import wallsensors
from IMI.libs.devices.key.key import KeyEvent, UISWNAME, UISWSTATE, UISWEXIT

lockfile = '/run/lock/imai/imi_main.lock'
daemonfile = '/run/lock/imai/imi_main.daemon'

### Thread ###
def testThreadLoop(id:int, stop_event:Event) -> None:
    try:
        testThreadLoopCnt:int = 0
        while not stop_event.is_set():
            print(f"Test thread:{testThreadLoopCnt}")
            testThreadLoopCnt += 1
            sleep(1)
    except KeyboardInterrupt:
        print("test Thread Keyboard Interrupt")
    finally:
        print("test Thread END")

def displayThreadLoop(pi:pigpio.pi, stop_event:Event, dispQ:Queue) -> None:
    try:
        dispThreadLoopCnt:int = 0
        dispstr:str
        while not stop_event.is_set():
            if not dispQ.empty():
                dispstr = dispQ.get()
                print(f"DISPLAY:{dispThreadLoopCnt}:{dispstr}")
                dispThreadLoopCnt += 1
            sleep(0.5)
    except KeyboardInterrupt:
        print("Display Thread Keyboard Interrupt")
    finally:
        print("Display Thread END")


### Multiprocess ###
def testProcessLoop(id:int, mp_stop_event:Event) -> None:
    try:
        print(f"id = {id}")
        testProcessLoopCnt:int = 0
        while not mp_stop_event.is_set():
            print(f"Test Loop:{testProcessLoopCnt}")
            sleep(1)
            testProcessLoopCnt += 1
    except KeyboardInterrupt:
        print("test Process Keyboard Interrupt")
    finally:
        print("test Process END")

def runLoop(pi, mp_stop_event:Event, jobQ:Queue) -> None:
    try:
        print("runLoop")
        testProcessLoopCnt:int = 0
        while not mp_stop_event.is_set():
            if not jobQ.empty():
                print(f"Test Loop:{testProcessLoopCnt}, main = {jobQ.get()}")
                testProcessLoopCnt += 1
            sleep(0.01)
    except KeyboardInterrupt:
        print("test Process Keyboard Interrupt")
    finally:
        print("test Process END")


def soundLoop(sound:Sound, mp_stop_event:Event, soundQ:Queue) -> None:
    try:
        while not mp_stop_event.is_set():
            if not soundQ.empty():
                sound.play(soundQ.get())
    except KeyboardInterrupt:
        print("sound Thread Keyboard Interrupt")
    finally:
        print("sound Thread END")


# Ctrl+Cで全てのスレッド/プロセスを正常終了させるためのシグナルハンドラ
def signal_handler(sig: int, frame, stop_event: Event, mp_stop_event:Event) -> None:
    print("\nCtrl+Cを受け取りました。すべてのスレッドとプロセスを終了します...")
    stop_event.set()  # スレッド用イベントをセット
    mp_stop_event.set()  # マルチプロセス用イベントをセット

# メイン関数でユーザー入力を処理
def main() -> bool:
    # マネージャーを使ってマルチプロセス間で共有できるイベントを作成
    mainExitSt:bool = False
    with Manager() as manager:
        stop_event = Event()  # スレッド用の終了イベント
        mp_stop_event = manager.Event()  # プロセス間で共有する終了イベント
        imipi = pigpio.pi()
        UIKeyE = KeyEvent(imipi)
        sound = Sound(imipi)
        jobCtrl = JobControler()
        job2CmdQ = Queue()
        displayQ = Queue()
        soundQ = Queue(maxsize=64)
        mainCnt:int = 0
        # スレッド
        test_thread: Thread = threading.Thread(target=testThreadLoop, args=(1, stop_event))
        sound_thread: Thread = threading.Thread(target=soundLoop, args=(sound, stop_event, soundQ))
        display_thread: Thread = threading.Thread(target=displayThreadLoop, args=(imipi, stop_event, displayQ))

        # プロセス
        test_process: Process = multiprocessing.Process(target=testProcessLoop, args=(2, mp_stop_event))
        runLoop_process: Process = multiprocessing.Process(target=runLoop, args=(imipi, mp_stop_event, job2CmdQ))

        # スレッドを開始
        test_thread.start()
        sound_thread.start()
        display_thread.start()

        # プロセスを開始
        test_process.start()
        runLoop_process.start()

        # シグナルハンドラを設定
        signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, stop_event, mp_stop_event))

        # ユーザーのスイッチ入力を待機
        try:
            exitflag:bool = False
            while not stop_event.is_set():
                updatef, exitSt, keysdic = UIKeyE.detector() 
                (jobSt, ejob, dispStr, soundP) = jobCtrl.Selector(updatef, exitSt, keysdic)
                if jobSt == JOB_STATE.ABORT:
                    print("####EXIT####")
                    mainExitSt = False
                    exitflag = True
                elif jobSt == JOB_STATE.HALT:
                    mainExitSt = True
                    exitflag = True
                if dispStr is not None:
                    displayQ.put(dispStr)
                if soundP is not None:
                    soundQ.put(soundP)
                if ejob is not None:
                    job2CmdQ.put(mainCnt)
                sleep(0.025)
                if exitflag:
                    sleep(1)
                    stop_event.set()  # スレッドの停止を指示
                    mp_stop_event.set()  # プロセスの停止を指示
                mainCnt += 1
        except KeyboardInterrupt:
            print("\nKeyboardInterruptが発生しました。")
            stop_event.set()
            mp_stop_event.set()
        finally:

            test_thread.join()
            sound_thread.join()
            display_thread.join()

            test_process.join()
            runLoop_process.join()

            print("すべてのスレッドとプロセスが正常に停止しました。")
            UIKeyE.close()
            imipi.stop()
    return mainExitSt

if __name__ == '__main__':
    if os.path.exists(lockfile):
        print("locked")

    else:
        rtn = main()
        if rtn:
            #正常に終了させた場合
            print("normal end")
            sys.exit(0)
        else:
            # 全ボタン押しなどで強制終了させた場合
            print("force end")
            sys.exit(1)
