import time
from enum import Enum
import RPi.GPIO as GPIO

# GPIO20 RAS2 SW0 
# GPIO26 RAS1 SW1 
# GPIO21 RAS0 SW2 

class UISW:
    SW0 = 20
    SW1 = 26
    SW2 = 21

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SW0, GPIO.IN)
        GPIO.setup(self.SW1, GPIO.IN)
        GPIO.setup(self.SW2, GPIO.IN)
    
    def __del__(self):
        GPIO.cleanup(self.SW0)
        GPIO.cleanup(self.SW1)
        GPIO.cleanup(self.SW2)
    
    def close(self):
        self.__del__()

    def read(self, swittch : int) -> bool:
        flag1 : bool = GPIO.input(swittch)
        time.sleep(0.025)
        flag2 : bool = GPIO.input(swittch)
        if flag1 == False and flag2 == False :
            return True
        else :
            return False
