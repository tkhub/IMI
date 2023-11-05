import RPi.GPIO as GPIO

class UILED:
    # LED3 RAS4 GPIO22
    # LED2 RAS5 GPIO23
    # LED1 RAS6 GPIO24
    # LED0 RAS7 GPIO25
    UILED0 = 25
    UILED1 = 24
    UILED2 = 23
    UILED3 = 18
    UILED_ON = True
    UILED_OFF = False
    __cnstcnt = 0
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.UILED0, GPIO.OUT)
        GPIO.setup(self.UILED1, GPIO.OUT)
        GPIO.setup(self.UILED2, GPIO.OUT)
        GPIO.setup(self.UILED3, GPIO.OUT)
        self.__cnstcnt += 1
    
    def __del__(self):
        if 0 < self.__cnstcnt:
            self.write(self.UILED0, self.UILED_OFF)
            self.write(self.UILED1, self.UILED_OFF)
            self.write(self.UILED2, self.UILED_OFF)
            self.write(self.UILED3, self.UILED_OFF)
            GPIO.cleanup(self.UILED0)
            GPIO.cleanup(self.UILED1)
            GPIO.cleanup(self.UILED2)
            GPIO.cleanup(self.UILED3)
            self.__cnstcnt -= 1
    
    def close(self):
        self.__del__()

    def write(self, ledch:int, level:bool) -> bool:
        if level == self.UILED_ON:
            GPIO.output(ledch, True)
        else :
            GPIO.output(ledch, False)
