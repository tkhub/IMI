import time
import sys
import os
import math
sys.path.append('../driver')

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import driver.mcp3xxx as mcp3xxx
import driver.wsnsled as wsnsled

class wallsensors:
    class adjustparam:
        gain:float
        offset:float
        threshold:float
        def __init__(self, g:float, o:float, t:float) -> None:
            self.gain = g
            self.offset = o
            self.threshold = t
        def normalize(self, snsval:float) -> float:
            if snsval < self.threshold:
                return None
            else:
                return snsval * self.gain + self.offset
            

    __cnstcnt :int = 0
    __ON_WAIT_TIME = 0.005
    __OFF_WAIT_TIME = 0.005
    def __init__(self) -> None:
        self.__ir_led = wsnsled.WSNSLED()
        self.__ir_tr = mcp3xxx.MCP3XXX()
        # self.PARAM_FL = self.adjustparam(-0.0439,149.99,200)
        self.PARAM_FL = self.adjustparam(-0.0440,145.99,200)
        self.PARAM_LL = self.adjustparam(-0.102,138.34,200)
        self.PARAM_RR = self.adjustparam(-0.0955,123.38,200)
        # self.PARAM_FR = self.adjustparam(-0.0202,136.76,200)
        self.PARAM_FR = self.adjustparam(-0.0202,135.76,200)
        self.__cnstcnt += 1

    def __del__(self):
        if 0 < self.__cnstcnt:
            self.__ir_led.close()
            self.__ir_tr.close()
            self.__cnstcnt -= 1

    def close(self):
        self.__del__()

    def readRaw(self) -> (float, float, float, float):
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
        FL = self.__ir_tr.read(self.__ir_tr.FL)
        self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_ON)
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_ON)
        time.sleep(self.__ON_WAIT_TIME)
        FL = self.__ir_tr.read(self.__ir_tr.FL) - FL
        self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_OFF)
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)

        # RR check
        time.sleep(self.__OFF_WAIT_TIME)
        RR = self.__ir_tr.read(self.__ir_tr.RR)
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_ON)
        time.sleep(self.__ON_WAIT_TIME)
        RR = self.__ir_tr.read(self.__ir_tr.RR) - RR
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)


        # FR
        time.sleep(self.__OFF_WAIT_TIME)
        FR = self.__ir_tr.read(self.__ir_tr.FR)
        self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_ON)
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_ON)
        time.sleep(self.__ON_WAIT_TIME)
        FR = self.__ir_tr.read(self.__ir_tr.FR) - FR
        self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_OFF)
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)

        # LL check
        time.sleep(self.__OFF_WAIT_TIME)
        LL = self.__ir_tr.read(self.__ir_tr.LL)
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_ON)
        time.sleep(self.__ON_WAIT_TIME)
        LL = self.__ir_tr.read(self.__ir_tr.LL) - LL
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)
        return (FL, LL, RR, FR)

    def readNormalized(self):
        snsval : float = self.readRaw()
        return  (self.PARAM_FL.normalize(snsval[0]),self.PARAM_LL.normalize(snsval[1]), self.PARAM_RR.normalize(snsval[2]),self.PARAM_FR.normalize(snsval[3]))
    

    def read(self) -> (bool, bool, bool, float, float, float):
        # 前、左右、傾きのズレ
        diff : float = 0.0
        length : float = 0.0
        degrees : float = 0.0
        snsval = self.readNormalized()
        print(snsval)
        MAZESIZE : float = 180
        MOUSEW:float = 87 #95 - 8
        if snsval[1] == None and snsval[2] == None:
            # 左壁センサ 右壁センサどちらもしきい値より低い場合、左右の計測は諦める
            diff = None
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
            diff =  snsval[1] - snsval[2]

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

