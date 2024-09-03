import RPi.GPIO as GPIO
import pigpio

class WSNSLED:
    LED_RR = 22
    LED_LL = 4
    LED_FR = 27
    LED_FL = 17
    WLED_ON = True
    WLED_OFF = False
    __constcnt = 0
    __pi:pigpio.pi
    def __init__(self) -> None:
        self.__pi = pigpio.pi()
        self.__pi.set_mode(self.LED_FL, pigpio.OUTPUT)
        self.__pi.set_mode(self.LED_FR, pigpio.OUTPUT)
        self.__pi.set_mode(self.LED_LL, pigpio.OUTPUT)
        self.__pi.set_mode(self.LED_RR, pigpio.OUTPUT)
        self.__pi.write(self.LED_FL, pigpio.LOW)
        self.__pi.write(self.LED_FR, pigpio.LOW)
        self.__pi.write(self.LED_LL, pigpio.LOW)
        self.__pi.write(self.LED_RR, pigpio.LOW)
        self.__constcnt += 1
    
    def __del__(self):
        if 0 < self.__constcnt:
            self.__pi.write(self.LED_FL, pigpio.LOW)
            self.__pi.write(self.LED_FR, pigpio.LOW)
            self.__pi.write(self.LED_LL, pigpio.LOW)
            self.__pi.write(self.LED_RR, pigpio.LOW)
            self.__pi.stop()
            self.__constcnt -= 1
    
    def close(self):
        self.__del__()

    def write(self, ledch:int, level:bool) -> bool:
        if level == self.WLED_ON:
            self.__pi.write(ledch, pigpio.HIGH)
            return True
        else :
            self.__pi.write(ledch, pigpio.LOW)
            return False
