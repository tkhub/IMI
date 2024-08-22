import imp
import sys
import os
from enum import Enum, auto
from typing import Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from .imimessage import RunCmd
from .libs.devices.motion.motion import runmotion

class RunExecutor:
    class __PARAMETER:
        class STRAIGHT:
            ANGLE_GAIN:float      = -0.3
            LENGTH_ADJUST:float   = 1.0
        # class __STOP:
        class FWALL:
            SPEED:float           = 10
            ANGLE_GAIN:float      = 1.0
            LENGTH_ADJUST:float   = 1.0
            SENSOR_OFFSET:float   = 0.0
    class __CONST:
        class STRAIGHT:
            PICH_LENGTH:float = 180.0
        class RIGHT_TURN:
            TURNANGLE:float = 90.0
            RADIUS:float = 90.0
        class LEFT_TURN:
            TURNANGLE:float = -90.0
            RADIUS:float = 90.0
        class U_TURN:
            TURNANGLE:float = -180.0

    __cnstcnt:int = 0
    __MOTION:runmotion
    def __init__(self):
        self.__MOTION = runmotion()
        self.__MOTION.start()
        self.__cnstcnt += 1

    def __del__(self):
        if self.__cnstcnt > 0:
            self.close()
            self.__cnstcnt -= 1

    def close(self):
        self.__MOTION.close()

    def move(   self, speed:float, motion:Optional[RunCmd] = None, \
                position:tuple[float, float, float] = (0,0,0),\
                sensor:tuple[Optional[float], Optional[float], Optional[float]] = (0.0, None, None), \
                walls:tuple[Optional[bool], Optional[bool], Optional[bool], Optional[bool]] = (None, None, None, None) ) -> tuple[float, float, float]:

        dx:float
        dy:float
        dd:float
        wsdiff:Optional[float]               = sensor[0]
        wsflength:Optional[float]   = sensor[1]
        wsfangle:Optional[float]    = sensor[2]
        # 直進コマンド
        if motion == RunCmd.STRAIGHT:
            if wsdiff is not None:
                adjust_deg:float = wsdiff * self.__PARAMETER.STRAIGHT.ANGLE_GAIN
            else:
                adjust_deg = 0
            length:float = self.__CONST.STRAIGHT.PICH_LENGTH * self.__PARAMETER.STRAIGHT.LENGTH_ADJUST
            self.__MOTION.run(speed_mmps=speed, degrees=adjust_deg, length=length, continueFlag=True)
        if motion == RunCmd.HALF_STRAGHT:
            length:float = 0.5 * self.__CONST.STRAIGHT.PICH_LENGTH * self.__PARAMETER.STRAIGHT.LENGTH_ADJUST
            self.__MOTION.run(speed_mmps=speed, degrees=0, length=length, continueFlag=True)
        # 右ターン
        elif motion == RunCmd.RIGHT_TURN:
            deg:float = self.__CONST.RIGHT_TURN.TURNANGLE
            length:float = 0.0
            # if wsfangle != None:
            #     adjust_deg:float = wsfangle  * self.__PARAMETER.FWALL.ANGLE_GAIN
            # if wsflength != None:
            #     length:float = wsflength - self.__PARAMETER.FWALL.LENGTH_ADJUST
            self.__MOTION.run(speed_mmps=speed, degrees=deg, radius=self.__CONST.RIGHT_TURN.RADIUS, continueFlag=True)
        elif motion == RunCmd.LEFT_TURN:
            deg:float = self.__CONST.LEFT_TURN.TURNANGLE
            length:float = 0.0
            # if wsfangle != None:
            #     adjust_deg:float = wsfangle  * self.__PARAMETER.FWALL.ANGLE_GAIN
            # if wsflength != None:
            #     length:float = wsflength - self.__PARAMETER.FWALL.LENGTH_ADJUST
            self.__MOTION.run(speed_mmps=speed, degrees=deg, radius=self.__CONST.LEFT_TURN.RADIUS, continueFlag=True)
        elif motion == RunCmd.STOP:
            # self.__MOTION.run(speed_mmps=speed, degrees=adjust_deg, length=length, continueFlag=True)
            # if wsfangle != None or wsflength != None:
            #     # ずれた分角度を補正する
            #     adj_angle:float = 0.0
            #     length:float = 0.0
            #     if wsfangle != None:
            #         adj_angle:float = wsfangle  * self.__PARAMETER.FWALL.ANGLE_GAIN
            #     if wsflength != None:
            #         length:float = wsflength - self.__PARAMETER.FWALL.LENGTH_ADJUST
            #     self.__MOTION.run(speed_mmps=self.__PARAMETER.FWALL.SPEED,degrees=adj_angle, length=length)
            self.__MOTION.pause()
        elif motion == RunCmd.U_TURN:

            # その他の命令時は停止
            # self.__MOTION.run(speed_mmps=speed, degrees=adjust_deg, length=length, continueFlag=True)
            self.__MOTION.pause()

        return self.__MOTION.position()


