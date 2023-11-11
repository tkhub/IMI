from concurrent.futures import ThreadPoolExecutor
import signal
import threading
from time import sleep
import sys

from libs.devices.driver import uiled as ULED
from libs.devices.driver import buzzer as UIBUZZER 
from libs.devices.driver import uisw as _uisw
sys.path.append("./libs/devices/")
from libs.devices.motion import motion
from libs.devices.wallsensors import wallsensors

# TODO: スイッチ入力を受け付けて走行を開始する
# TODO: センサの値を読み込んで走行する(走行＝左右の壁を判断して直線をしっかり走る。迷路情報により)
# TODO: 迷路情報から経路を判断し、司令する。

class Run:
    def __init__(self) -> None:
        self.MVMOTION = motion.motion()
        self.WLSNS = wallsensors.wallsensors()
        self.MAZE_SIZE : float = 180.0


def main():
    uisw = _uisw.UISW()
    UILED = ULED.UILED()
    UIBZ = UIBUZZER.buzzer.UIBZ()
    MVMOTION = motion.motion()
    WLSNS = wallsensors.wallsensors()
    while True:
        if uisw.read(uisw.SW0) == True:
            break;
        sleep(0.01)
    
    UIBZ.play(2000,pauseLength=1)
    print("3")
    UIBZ.play(440,pauseLength=0.5)
    sleep(0.5)
    print("2")
    UIBZ.play(600,pauseLength=0.5)
    sleep(0.5)
    print("1")
    UIBZ.play(800,pauseLength=0.5)
    sleep(0.5)
    print("GO")
    UIBZ.play(1000,pauseLength=0.5)
    MVMOTION.start()
    sleep(0.05)
    MVMOTION.run(speed_mmps=100, degrees = 0, length=MAZE_SIZE/2, continueFlag=False)
    sleep(10)
   #  MVMOTION.run(speed_mmps= 0, degrees = 90, runTime = 0.5, continueFlag=False)
    while True:
        wsns = WLSNS.read()
        # print(wsns)
        if wsns[1] == False:
            # 前が空いてる
            print("^")
            MVMOTION.run(speed_mmps=150, degrees = 0, length=MAZE_SIZE, continueFlag=False)
        elif wsns[2] == False:
            # 右が空いてる
            print("->")
            MVMOTION.run(speed_mmps=150, degrees = 0, length=MAZE_SIZE, continueFlag=False)
            MVMOTION.run(speed_mmps=0, degrees = 90, runTime=0.25, continueFlag=False)
        elif wsns[0] == False:
            # 左が空いてる
            print("<-")
            MVMOTION.run(speed_mmps=150, degrees = 0, length=MAZE_SIZE, continueFlag=False)
            MVMOTION.run(speed_mmps=0, degrees = -90, runTime=0.25, continueFlag=False)
        else:
            # Uターン
            print("U")
            MVMOTION.run(speed_mmps=0, degrees = 180, runTime=0.5, continueFlag=False)
        if uisw.read(uisw.SW0) == True  and uisw.read(uisw.SW1) == True and uisw.read(uisw.SW2) == True :
            break
    MVMOTION.stop()
    sleep(1)
    uisw.close()
    UILED.close()
    UIBZ.close()
    MVMOTION.close()
    WLSNS.close()

if __name__ == '__main__':
    main()
    
