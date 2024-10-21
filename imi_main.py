import threading
import multiprocessing
from time import sleep, clock_gettime_ns
import signal
import sys
from threading import Thread, Event
from multiprocessing import Process, Manager


import pigpio

from IMI.libs.devices.key.key import KeyEvent, UISWNAME, UISWSTATE



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

# # センサーの監視関数 (センサーIDを引数に取る)
# def sensor_monitor(sensor_id: int, stop_event: Event) -> None:
#     try:
#         while not stop_event.is_set():  # stop_eventがセットされるまでループ
#             print(f"センサー {sensor_id} を監視しています...")
#             time.sleep(1)
#     except KeyboardInterrupt:
#         pass
#     print(f"センサースレッド {sensor_id} を停止します")

# モーターの制御関数 (モーターIDを引数に取る)
# def motor_control(motor_id: int, stop_event: multiprocessing.Event) -> None:
#     try:
#         while not stop_event.is_set():  # stop_eventがセットされるまでループ
#             print(f"モーター {motor_id} を制御しています...")
#             time.sleep(1)
#     except KeyboardInterrupt:
#         pass
#     print(f"モータープロセス {motor_id} を停止します")

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
        # センサーIDとモーターID
        sensor_id: int = 1
        motor_id: int = 1
        display_id: int = 1
        speaker_id: int = 1

        # センサー監視とディスプレイ制御、スピーカー制御のスレッドを作成
        # display_thread: Thread = threading.Thread(target=display_control, args=(display_id, stop_event))
        # speaker_thread: Thread = threading.Thread(target=speaker_control, args=(speaker_id, stop_event))
        test_thread: Thread = threading.Thread(target=testThreadLoop, args=(1, stop_event))

        # モーター制御のプロセスを作成
        # motor_process: Process = multiprocessing.Process(target=motor_control, args=(motor_id, mp_stop_event))
        test_process: Process = multiprocessing.Process(target=testProcessLoop, args=(motor_id, mp_stop_event))

        # スレッドを開始
        # display_thread.start()
        # speaker_thread.start()
        test_thread.start()

        # プロセスを開始
        # motor_process.start()
        test_process.start()

        # シグナルハンドラを設定
        signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, stop_event, mp_stop_event))

        # ユーザーのスイッチ入力を待機
        try:
            while not stop_event.is_set():
                update, exitf, swstate = UIKeyE.detector() 
                # user_input = input("コマンドを入力してください (q で終了): ").strip()
                # if user_input == 'q':
                #     print("終了コマンドを受け取りました...")
                #     stop_event.set()  # スレッドの停止を指示
                #     mp_stop_event.set()  # プロセスの停止を指示
                # elif user_input == 's':
                #     print("スイッチを操作しました。")
                #     # ここにスイッチ入力に対する処理を追加可能
                # else:
                #     print(f"無効な入力: {user_input}")
                if exitf:
                    print("####EXIT####")
                    stop_event.set()  # スレッドの停止を指示
                    mp_stop_event.set()  # プロセスの停止を指示
                elif update:
                    print(f"{swstate}")
                else:
                    sleep(0.01)
        except KeyboardInterrupt:
            print("\nKeyboardInterruptが発生しました。")
            stop_event.set()
            mp_stop_event.set()
        finally:

            # スレッドが終了するのを待機
            # sensor_thread.join()
            # display_thread.join()
            # speaker_thread.join()
            test_thread.join()

            # プロセスが終了するのを待機
            # motor_process.join()
            test_process.join()

            print("すべてのスレッドとプロセスが正常に停止しました。")
            UIKeyE.close()
            imipi.stop()

if __name__ == '__main__':
    main()
