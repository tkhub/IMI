from optparse import Option
import time
from typing import Optional
import pigpio

class UIBZ:

    __PIN = 19
    __MIN_HZ = 40
    __MAX_HZ = 10000
    __STOP_DUTY_VAL = 255
    __PLAY_DUTY_VAL = 128
    __cnstcnt : int = 0
    __PIGPIO:pigpio.pi
    def __init__(self, pi:pigpio.pi) -> None:
        self.__PIGPIO = pi
        self.__PIGPIO.set_PWM_dutycycle(self.__PIN, self.__STOP_DUTY_VAL)
        self.__PIGPIO.set_PWM_frequency(self.__PIN, 1000)
        self.__cnstcnt += 1


    def __del__(self):
        if 0 < self.__cnstcnt:
            self.__PIGPIO.stop()
            self.__cnstcnt -= 1

    def close(self):
        self.__del__()

    def play(self, freq:int = 0, playLength:Optional[float] = None, pauseLength:Optional[float] = None):
        if self.__MAX_HZ < freq:
            freq = self.__MAX_HZ
        if freq < self.__MIN_HZ:
            self.__PIGPIO.set_PWM_dutycycle(self.__PIN, self.__STOP_DUTY_VAL)
        else:
            self.__PIGPIO.set_PWM_dutycycle(self.__PIN, self.__PLAY_DUTY_VAL)
            self.__PIGPIO.set_PWM_frequency(self.__PIN, freq)

        if playLength is None:
            # 連続音なので何もしないまま抜ける
            pass
        else:
            # 長さが決まっているのでスリープ
            time.sleep(playLength)
            if pauseLength is not None:
                self.__PIGPIO.set_PWM_dutycycle(self.__PIN, self.__STOP_DUTY_VAL)
                if pauseLength > 0.01:
                    time.sleep(pauseLength)