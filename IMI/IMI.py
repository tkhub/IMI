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
sys.path.append("./libs/app/")
from libs.app.maze import maze

# TODO: スイッチ入力を受け付けて走行を開始する
# TODO: センサの値を読み込んで走行する(走行＝左右の壁を判断して直線をしっかり走る。迷路情報により)
# TODO: 迷路情報から経路を判断し、司令する。

class Run:
    __cnstcnt:int = 0
    __X_GAIN = -0.3
    __STHF_LEN = 83.0
    __TURN_HFST_LEN = 89.0
    __R_TRUN_ANGL = +87.5
    __L_TRUN_ANGL = -87.5
    __U_TRUN_ANGL = +180.0
    def __init__(self) -> None:
        self.MVMOTION = motion.motion()
        self.WLSNS = wallsensors.wallsensors()
        self.MAZE_SIZE : float = 180.0
        self.__cnstcnt  += 1
        self.MVMOTION.start()
    
    def __del__(self):
        self.close()
    
    def close(self):
        if 0 < self.__cnstcnt:
            self.MVMOTION.stop()
            self.MVMOTION.close()
            self.WLSNS.close()

    def straight(self, speed:float, grids:int, contFlag:bool = True):
        adjust_deg:float = 0
        wsns = (False, False, False, 0.0, 0.0, 0.0)
        for i in range(grids * 2 -1):
            wsns = self.WLSNS.read()
            adjust_deg = wsns[3] * self.__X_GAIN
            print(adjust_deg)
            self.MVMOTION.run(speed_mmps=speed, degrees = adjust_deg, length=self.__STHF_LEN, continueFlag=True)
        self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.__STHF_LEN, continueFlag=contFlag)
        pos = self.MVMOTION.position()
        return (wsns[0], wsns[1],wsns[2],wsns[3],wsns[4],wsns[5], pos[0], pos[1], pos[2])

    def straight_hf(self, speed:float,contFlag:bool = True):
        wsns = self.WLSNS.read()
        self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.__STHF_LEN, continueFlag=contFlag)
        pos = self.MVMOTION.position()
        return (wsns[0], wsns[1],wsns[2],wsns[3],wsns[4],wsns[5], pos[0], pos[1], pos[2])

    def left(self, speed:float):
        self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.__TURN_HFST_LEN, continueFlag=False)
        sleep(0.1)
        self.MVMOTION.run(speed_mmps=speed, degrees = self.__L_TRUN_ANGL, runTime=0.5, continueFlag=False)
        sleep(0.1)
        self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.MAZE_SIZE/2, continueFlag=False)
        wsns = self.WLSNS.read()
        pos = self.MVMOTION.position()
        return (wsns[0], wsns[1],wsns[2],wsns[3],wsns[4],wsns[5], pos[0], pos[1], pos[2])

    def right(self, speed:float):
        self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.MAZE_SIZE/2, continueFlag=False)
        sleep(0.1)
        self.MVMOTION.run(speed_mmps=speed, degrees = self.__R_TRUN_ANGL, runTime=0.5, continueFlag=False)
        sleep(0.1)
        self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.MAZE_SIZE/2, continueFlag=False)
        wsns = self.WLSNS.read()
        pos = self.MVMOTION.position()
        return (wsns[0], wsns[1],wsns[2],wsns[3],wsns[4],wsns[5], pos[0], pos[1], pos[2])

    def u_turn(self, speed:float):
        self.MVMOTION.run(speed_mmps=speed, degrees = self.__U_TRUN_ANGL, runTime=1.5, continueFlag=False)
        self.MVMOTION.run(speed_mmps=-speed, degrees = 0, length=self.MAZE_SIZE/2, continueFlag=False)
        wsns = self.WLSNS.read()
        pos = self.MVMOTION.position()
        return (wsns[0], wsns[1],wsns[2],wsns[3],wsns[4],wsns[5], pos[0], pos[1], pos[2])

    def l_turn(self, mtime:float = 1.0):
        self.MVMOTION.run(speed_mmps=0, degrees = self.__L_TRUN_ANGL, runTime=mtime, continueFlag=False)
        sleep(0.5)

    def r_turn(self, mtime:float = 1.0):
        self.MVMOTION.run(speed_mmps=0, degrees = self.__R_TRUN_ANGL, runTime=mtime, continueFlag=False)
        sleep(0.5)


def main():
    uisw = _uisw.UISW()
    UILED = ULED.UILED()
    UIBZ = UIBUZZER.buzzer.UIBZ()
    rx:float = 89.99
    ry:float = 89.99
    rdeg:float = 0.0
    offset_f = 89
    Fullmaze = maze.Maze(maze_size=(16,16), goal=(7,7))
    MRUN = Run()
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
    MRUN.straight(speed=200, grids = 5, contFlag = False)
    uisw.close()
    UILED.close()
    UIBZ.close()

if __name__ == '__main__':
    main()
    
