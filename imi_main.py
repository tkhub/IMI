import threading
import multiprocessing
from time import sleep, clock_gettime_ns
import signal
import sys
from threading import Thread, Event
from multiprocessing import Process, Manager, Queue


import pigpio

from IMI.imimessage import JOB, ExecJob, RunCmd, SoundPattern
from IMI.runcommander import commandSetter
from IMI.uisystem import JobControler, Sound
from IMI.libs.devices.wallsensors.wallsensors import wallsensors
from IMI.libs.devices.key.key import KeyEvent, UISWNAME, UISWSTATE

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
def main():
    # マネージャーを使ってマルチプロセス間で共有できるイベントを作成
    with Manager() as manager:
        stop_event = Event()  # スレッド用の終了イベント
        mp_stop_event = manager.Event()  # プロセス間で共有する終了イベント
        imipi = pigpio.pi()
        UIKeyE = KeyEvent(imipi)
        sound = Sound(imipi)
        job2CmdQ = Queue()
        soundQ = Queue(maxsize=64)
        mainCnt:int = 0
        # スレッド
        test_thread: Thread = threading.Thread(target=testThreadLoop, args=(1, stop_event))
        sound_thread: Thread = threading.Thread(target=soundLoop, args=(sound, stop_event, soundQ))
        

        # プロセス
        test_process: Process = multiprocessing.Process(target=testProcessLoop, args=(2, mp_stop_event))
        runLoop_process: Process = multiprocessing.Process(target=runLoop, args=(imipi, mp_stop_event, job2CmdQ))

        # スレッドを開始
        test_thread.start()
        sound_thread.start()

        # プロセスを開始
        test_process.start()
        runLoop_process.start()

        # シグナルハンドラを設定
        signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, stop_event, mp_stop_event))

        # ユーザーのスイッチ入力を待機
        try:
            while not stop_event.is_set():
                update, exitf, swstate = UIKeyE.detector() 
                if exitf:
                    print("####EXIT####")
                    stop_event.set()  # スレッドの停止を指示
                    mp_stop_event.set()  # プロセスの停止を指示
                elif update:
                    print(f"{swstate}")
                    job2CmdQ.put(mainCnt)
                    soundQ.put(SoundPattern.OK_0)
                else:
                    sleep(0.025)
                mainCnt += 1
        except KeyboardInterrupt:
            print("\nKeyboardInterruptが発生しました。")
            stop_event.set()
            mp_stop_event.set()
        finally:

            test_thread.join()
            sound_thread.join()

            test_process.join()
            runLoop_process.join()

            print("すべてのスレッドとプロセスが正常に停止しました。")
            UIKeyE.close()
            imipi.stop()

if __name__ == '__main__':
    main()
