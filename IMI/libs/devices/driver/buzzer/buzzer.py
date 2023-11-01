import time
import pigpio

class UIBZ:

    __PIN = 19
    __MIN_HZ = 40
    __MAX_HZ = 10000
    __STOP_DUTY_VAL = 255
    __PLAY_DUTY_VAL = 128
    def __init__(self) -> None:
        self.__PIGPIO = pigpio.pi()
        self.__PIGPIO.set_PWM_dutycycle(self.__PIN, self.__STOP_DUTY_VAL)
        self.__PIGPIO.set_PWM_frequency(self.__PIN, 1000)

    def __del__(self):
        self.__PIGPIO.stop()

    def close(self):
        self.__del__()

    def play(self, freq:int = 0, playLength:float = None, pauseLength:float = None):
        if self.__MAX_HZ < freq:
            freq = self.__MAX_HZ
        if freq < self.__MIN_HZ:
            self.__PIGPIO.set_PWM_dutycycle(self.__PIN, self.__STOP_DUTY_VAL)
        else:
            self.__PIGPIO.set_PWM_dutycycle(self.__PIN, self.__PLAY_DUTY_VAL)
            self.__PIGPIO.set_PWM_frequency(self.__PIN, freq)

        if playLength != None:
            time.sleep(playLength)
        if pauseLength!= None:
            time.sleep(pauseLength)
            self.__PIGPIO.set_PWM_dutycycle(self.__PIN, self.__STOP_DUTY_VAL)