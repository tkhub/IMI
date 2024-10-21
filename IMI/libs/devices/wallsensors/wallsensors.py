import time
import sys
import os
import math
from typing import Optional
from enum import Enum, IntEnum
import pigpio
sys.path.append('../driver')

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
# import driver.mcp3xxx as mcp3xxx
# import driver.wsnsled as wsnsled
# from IMI.libs.devices.driver import mcp3xxx
from driver.mcp3xxx.mcp3xxx import MCP3208 as ADC, MCP3XXX_OLD as ADCO
from driver.wsnsled.wsnsled import WSNSLED as WLED

class wallsensors:
    class adjustparam:
        gain:float
        offset:float
        threshold:float
        def __init__(self, g:float, o:float, t:float) -> None:
            self.gain = g
            self.offset = o
            self.threshold = t

        def normalize(self, snsval:float) -> Optional[float]:
            if snsval < self.threshold:
                return None
            else:
                return snsval * self.gain + self.offset
            
    class SNSCH(IntEnum):
        FL = 1
        FR = 2
        RR = 3
        LL = 0
    __cnstcnt :int = 0
    __ON_WAIT_TIME =    0.001
    __OFF_WAIT_TIME =   0.001
    def __init__(self, pi:pigpio.pi) -> None:
        # self.__ir_led = wsnsled.WSNSLED()
        # self.__ir_tr = mcp3xxx.MCP3XXX()
        # self.__ir_tr = ADC(pi=pi, spichannel=ADC.SPIchannel.CH_0, speed=50000)
        self.__ir_tr = ADCO(spi_channel=0, speed=500000, bit = 12, chnum=8)
        self.__ir_led = WLED(pi=pi)

        # self.PARAM_FL = self.adjustparam(-0.0439,149.99,200)
        # self.PARAM_FL = self.adjustparam(-0.0440,145.99,200) +5mm
        self.PARAM_FL = self.adjustparam(-0.0439,154.99,150)
        self.PARAM_LL = self.adjustparam(-0.102,138.34, 200)
        self.PARAM_RR = self.adjustparam(-0.0955,123.38, 220)
        # self.PARAM_FR = self.adjustparam(-0.0202,136.76,200)
        # self.PARAM_FR = self.adjustparam(-0.0202,135.76,200) +5mm
        self.PARAM_FR = self.adjustparam(-0.0202,147.76,150)
        self.__cnstcnt += 1

    def __del__(self):
        if 0 < self.__cnstcnt:
            self.__ir_led.close()
            self.__ir_tr.close()
            self.__cnstcnt -= 1

    def close(self):
        self.__del__()

    def readRaw(self) -> tuple[float, float, float, float]:
        #          Q4↖    ↗Q3         
        #          CH0       CH3        
        #          D12       D6         
        #                               
        #                               
        #   Q5↑                   ↑Q2 
        #  CH1                      CH2 
        #  D13                      D5  
        #  FL(17)                   FR(27)       
        LL : int = 0
        FL : int = 0
        FR : int = 0
        RR : int = 0
        self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_OFF)
        self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_OFF)
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)

        # FL check
        time.sleep(self.__OFF_WAIT_TIME)
        # FL = self.__ir_tr.read(self.SNSCH.FL)
        FL = self.__ir_tr.read(self.SNSCH.FL)
        # 前センサは左右干渉する可能性があるので同時点灯
        self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_ON)
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_ON)
        time.sleep(self.__ON_WAIT_TIME)
        FL = self.__ir_tr.read(self.SNSCH.FL) - FL
        self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_OFF)
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)

        # RR check
        time.sleep(self.__OFF_WAIT_TIME)
        RR = self.__ir_tr.read(self.SNSCH.RR)
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_ON)
        time.sleep(self.__ON_WAIT_TIME)
        RR = self.__ir_tr.read(self.SNSCH.RR) - RR
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)


        # FR
        time.sleep(self.__OFF_WAIT_TIME)
        FR = self.__ir_tr.read(self.SNSCH.FR)
        self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_ON)
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_ON)
        time.sleep(self.__ON_WAIT_TIME)
        FR = self.__ir_tr.read(self.SNSCH.FR) - FR
        self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_OFF)
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)

        # LL check
        time.sleep(self.__OFF_WAIT_TIME)
        LL = self.__ir_tr.read(self.SNSCH.LL)
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_ON)
        time.sleep(self.__ON_WAIT_TIME)
        LL = self.__ir_tr.read(self.SNSCH.LL) - LL
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)
        return (FL, LL, RR, FR)

    def readNormalized(self):
        snsval : tuple[float, float, float, float] = self.readRaw()
        return  (self.PARAM_FL.normalize(snsval[0]),self.PARAM_LL.normalize(snsval[1]), self.PARAM_RR.normalize(snsval[2]),self.PARAM_FR.normalize(snsval[3]))
    
    def read(self) -> tuple[Optional[bool], Optional[bool], Optional[bool], float, Optional[float], Optional[float]]:
        """_summary_

        Returns:
            tuple[Optional[bool], Optional[bool], Optional[bool], float, Optional[float], Optional[float]]: 左壁の有無, 前壁の有無, 右壁の有無, ズレ、前壁との距離, 傾き
        """        # 前、左右、傾きのズレ
        diff : float = 0.0
        length : Optional[float] = 0.0
        degrees : Optional[float] = 0.0
        snsval = self.readNormalized()
        MAZESIZE : float = 180
        MOUSEW:float = 87 #95 - 8
        if snsval[1] != None and snsval[2] != None:
            # 左右の壁の差からズレを算出する
            diff =  snsval[1] - snsval[2]
        elif snsval[1] != None and snsval[2] == None:
            # 左壁センサのみ信用できる場合、左壁から求める
            #diff = (MOUSEW - MAZESIZE)/2 + snsval[1]
            # 86 
            # 90 - 
            diff = -((MAZESIZE)/2 - snsval[1])
        elif snsval[1] == None and snsval[2] != None:
            # 右壁センサのみ信用できる場合、右壁から求める
            # diff = (MOUSEW - MAZESIZE)/2 - snsval[2]
            diff = (MAZESIZE)/2 - snsval[2]
        else :
            # 左壁センサ 右壁センサどちらもしきい値より低い場合、左右の計測は諦める
            diff = 0.0 

        if snsval[0] == None or snsval[3] == None:
            length = None
            degrees = None
        else :
            length = (snsval[0] + snsval[3]) / 2
            degrees = math.degrees(math.asin((snsval[3] - snsval[0])/MOUSEW))

        if snsval[0] == None or snsval[3] == None:
            f_sns = False
        else :
            f_sns = True

        if snsval[1] == None:
            l_sns = False
        else :
            l_sns = True
        
        if snsval[2] == None:
            r_sns = False
        else :
            r_sns = True

        return (l_sns, f_sns, r_sns, diff, length, degrees,)

