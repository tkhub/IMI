import time
from enum import Enum
from typing import Optional, Callable
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
    __CHTWAIT:float = 0.025
    def __init__(self, pi:pigpio.pi, intrFuncSW0:Optional[Callable[[int,bool,int], None]] = None, intrFuncSW1:Optional[Callable[[int,bool,int], None]] = None,intrFuncSW2:Optional[Callable[[int,bool,int], None]] = None) -> None:
        self.__pi = pi
        self.__pi.set_mode(self.SW0,pigpio.INPUT)
        self.__pi.set_mode(self.SW1,pigpio.INPUT)
        self.__pi.set_mode(self.SW2,pigpio.INPUT)
        self.__pi.set_pull_up_down(self.SW0, pigpio.PUD_UP)
        self.__pi.set_pull_up_down(self.SW1, pigpio.PUD_UP)
        self.__pi.set_pull_up_down(self.SW2, pigpio.PUD_UP)
        
        if intrFuncSW0 is not None:
            self.__cbSW0 = self.__pi.callback(self.SW0, pigpio.EITHER_EDGE, intrFuncSW0)
        if intrFuncSW1 is not None:
            self.__cbSW1 = self.__pi.callback(self.SW1, pigpio.EITHER_EDGE, intrFuncSW1)
        if intrFuncSW2 is not None:
            self.__cbSW2 = self.__pi.callback(self.SW2, pigpio.EITHER_EDGE, intrFuncSW2)
        self.__cnstcnt += 1
    
    def __del__(self):
        if 0 < self.__cnstcnt:
            self.__cnstcnt -= 1
    
    def close(self):
        self.__del__()

    def read(self, swittch : int) -> bool:
        flag1 : bool = bool(self.__pi.read(swittch))
        time.sleep(self.__CHTWAIT)
        flag2 : bool = bool(self.__pi.read(swittch))
        if flag1 == False and flag2 == False :
            return True
        else :
            return False
