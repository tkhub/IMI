import time
from enum import Enum
import RPi.GPIO as GPIO
import pigpio

# GPIO20 RAS2 SW0 
# GPIO26 RAS1 SW1 
# GPIO21 RAS0 SW2 

class UISW:
    SW0 = 20
    SW1 = 26
    SW2 = 21
    __cnstcnt : int = 0
    __pi:pigpio.pi
    def __init__(self) -> None:
        self.__pi =pigpio.pi()
        self.__pi.set_mode(self.SW0,pigpio.INPUT)
        self.__pi.set_mode(self.SW1,pigpio.INPUT)
        self.__pi.set_mode(self.SW2,pigpio.INPUT)
        self.__pi.set_pull_up_down(self.SW0, pigpio.PUD_UP)
        self.__pi.set_pull_up_down(self.SW1, pigpio.PUD_UP)
        self.__pi.set_pull_up_down(self.SW2, pigpio.PUD_UP)

        self.__cnstcnt += 1
    
    def __del__(self):
        if 0 < self.__cnstcnt:
            self.__pi.stop()
            self.__cnstcnt -= 1
    
    def close(self):
        self.__del__()

    def read(self, swittch : int) -> bool:
        flag1 : bool = bool(self.__pi.read(swittch))
        time.sleep(0.01)
        flag2 : bool = bool(self.__pi.read(swittch))
        if flag1 == False and flag2 == False :
            return True
        else :
            return False
