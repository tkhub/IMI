import sys
import os
from time import sleep, clock_gettime_ns
from enum import Enum, auto

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from driver.buzzer.buzzer import UIBZ as DRV_BUZZER

class Pattern(Enum):
    NONE_TONE   = 0
    EXIT_0      = auto()
    OK_0        = auto()
    CANCEL_0    = auto()
    SELECT_0    = auto()
    ERROR_0     = auto()

class Sound:
    __cnstcnt : int = 0
    __UIBZ : DRV_BUZZER

    def __init__(self) -> None:
        self.__UIBZ = DRV_BUZZER()
        self.__cnstcnt += 1
    
    def __del__(self):
        self.__UIBZ.close()
        self.__cnstcnt -= 1
    
    def close(self):
        self.__del__()
    
    def play(self, soundPattern:Pattern) -> None:
        if soundPattern == Pattern.OK_0:
            self.__UIBZ.play(freq=1760, playLength=0.5,pauseLength=0.01)
            self.__UIBZ.play(freq=2400, playLength=0.5,pauseLength=0.01)

        elif soundPattern == Pattern.CANCEL_0:
            self.__UIBZ.play(freq=880, playLength=0.1,pauseLength=0.01)
            self.__UIBZ.play(freq=440, playLength=0.1,pauseLength=0.01)

        elif soundPattern == Pattern.SELECT_0:
            self.__UIBZ.play(freq=270, playLength=0.25,pauseLength=0.01)

        elif soundPattern == Pattern.EXIT_0:
            self.__UIBZ.play(freq=270, playLength=0.5,pauseLength=0.01)
            self.__UIBZ.play(freq=880, playLength=0.25,pauseLength=0.01)
            self.__UIBZ.play(freq=270, playLength=0.5,pauseLength=0.01)
            self.__UIBZ.play(freq=880, playLength=0.25,pauseLength=0.01)

        elif soundPattern == Pattern.ERROR_0:
            self.__UIBZ.play(freq=270, playLength=0.5,pauseLength=0.01)

        else:
            self.__UIBZ.play(freq=440, playLength=1,pauseLength=0.1)