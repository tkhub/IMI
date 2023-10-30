import time
# from driver import wsnsled
# from driver import mcp3xxx
import sys
sys.path.append('../')
import driver.mcp3xxx as mcp3xxx
import driver.wsnsled as wsnsled

class wallsensors:
    class calibration:
        gain:float
        offset:float
    __cnstcnt :int = 0
    __ON_WAIT_TIME = 0.005
    __OFF_WAIT_TIME = 0.005
    def __init__(self) -> None:
        self.__ir_led = wsnsled.WSNSLED()
        self.__ir_tr = mcp3xxx.MCP3XXX()
        self.__cnstcnt += 1

    def __del__(self):
        self.close()

    def close(self):
        if 0 < self.__cnstcnt:
            self.__ir_led.close()
            self.__ir_tr.close()
            self.__cnstcnt -= 1

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
        time.sleep(0.005)
        FL = self.__ir_tr.read(self.__ir_tr.FL)
        self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_ON)
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_ON)
        time.sleep(0.005)
        FL = self.__ir_tr.read(self.__ir_tr.FL) - FL
        self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_OFF)
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)

        # RR check
        time.sleep(0.005)
        RR = self.__ir_tr.read(self.__ir_tr.RR)
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_ON)
        time.sleep(0.005)
        RR = self.__ir_tr.read(self.__ir_tr.RR) - RR
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)


        # FR
        time.sleep(0.005)
        FR = self.__ir_tr.read(self.__ir_tr.FR)
        self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_ON)
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_ON)
        time.sleep(0.005)
        FR = self.__ir_tr.read(self.__ir_tr.FR) - FR
        self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_OFF)
        self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)

        # LL check
        time.sleep(0.005)
        LL = self.__ir_tr.read(self.__ir_tr.LL)
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_ON)
        time.sleep(0.005)
        LL = self.__ir_tr.read(self.__ir_tr.LL) - LL
        self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)

        return [FL, LL, RR, FR]

        
    # def _testRead(self, onoffch : int) -> [int, int, int, int]:
    #     match onoffch:
    #         case 0:
    #             self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)
    #         case 1:
    #             self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_ON)
    #             self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)
    #             print(self.__ir_tr.read(self.__ir_tr.FL))
    #         case 2:
    #             self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_ON)
    #             self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)
    #             print(self.__ir_tr.read(self.__ir_tr.FR))
    #         case 3:
    #             self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_ON)
    #             self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)
    #             print(self.__ir_tr.read(self.__ir_tr.LL))
    #         case 4:
    #             self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_ON)
    #             print(self.__ir_tr.read(self.__ir_tr.RR))
    #         case 5:
    #             self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_ON)
    #             self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_ON)
    #             self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_ON)
    #             self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_ON)
    #         case _:
    #             self.__ir_led.write(self.__ir_led.LED_FL, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_FR, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_LL, self.__ir_led.WLED_OFF)
    #             self.__ir_led.write(self.__ir_led.LED_RR, self.__ir_led.WLED_OFF)
    #     sensor = self.__ir_tr.read()
    #     return sensor[0:4]
