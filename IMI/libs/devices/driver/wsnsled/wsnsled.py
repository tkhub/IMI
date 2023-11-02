import RPi.GPIO as GPIO

class WSNSLED:
    # LED3 RAS4 GPIO22
    # LED2 RAS5 GPIO23
    # LED1 RAS6 GPIO24
    # LED0 RAS7 GPIO25
    LED_RR = 22
    LED_LL = 4
    LED_FR = 27
    LED_FL = 17
    WLED_ON = True
    WLED_OFF = False
    __constcnt = 0
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_RR, GPIO.OUT)
        GPIO.setup(self.LED_LL, GPIO.OUT)
        GPIO.setup(self.LED_FR, GPIO.OUT)
        GPIO.setup(self.LED_FL, GPIO.OUT)
        self.__constcnt += 1
    
    def __del__(self):
        if 0 < self.__constcnt:
            GPIO.cleanup(self.LED_RR)
            GPIO.cleanup(self.LED_LL)
            GPIO.cleanup(self.LED_FR)
            GPIO.cleanup(self.LED_FL)
            self.__constcnt -= 1
    
    def close(self):
        self.__del__()

    def write(self, ledch:int, level:bool) -> bool:
        if level == self.WLED_ON:
            GPIO.output(ledch, True)
        else :
            GPIO.output(ledch, False)
