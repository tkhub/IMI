import time
import RPi.GPIO as GPIO

class UIBZ:

    __UIBZ_PIN = 19
    __UIBZ_MIN_HZ = 40
    __UIBZ_MAX_HZ = 10000
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__UIBZ_PIN, GPIO.OUT)
        self.__UIBZ_START = False

    def __del__(self):
        GPIO.cleanup(self.__UIBZ_PIN)

    def close(self):
        self.__del__()

    def play(self, freq:int = 1000, playLength:float = None, pauseLength:float = None):
        if self.__UIBZ_MAX_HZ < freq:
            freq = self.__UIBZ_MAX_HZ

        if self.__UIBZ_START == False:
            self.__UIBZ_START = True
            if freq < self.__UIBZ_MIN_HZ:
                self.__UIBZ= GPIO.PWM(self.__UIBZ_PIN, self.__UIBZ_MIN_HZ)
                self.__UIBZ.start(100)
            else :
                self.__UIBZ= GPIO.PWM(self.__UIBZ_PIN, freq)
                self.__UIBZ.start(50)
        else:
            if freq < self.__UIBZ_MIN_HZ:
                self.__UIBZ.ChangeDutyCycle(100)
            else :
                self.__UIBZ.ChangeFrequency(freq)
                self.__UIBZ.ChangeDutyCycle(50)
        if playLength != None:
            time.sleep(playLength)
        if pauseLength!= None:
            time.sleep(pauseLength)
            self.__UIBZ.ChangeDutyCycle(100)