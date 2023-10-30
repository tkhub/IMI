import sys
import time
from wsnsled import WSNSLED

def main():
    WLED = WSNSLED()
    state:int = 0
    try:
        while True:
            match state:
                case 0:
                    WLED.write(WLED.LED_FL, WLED.WLED_OFF)
                    WLED.write(WLED.LED_FR, WLED.WLED_OFF)
                    WLED.write(WLED.LED_RR, WLED.WLED_OFF)
                    WLED.write(WLED.LED_LL, WLED.WLED_OFF)
                    print("OFF")
                    time.sleep(4)
                    state = 1

                case 1:
                    WLED.write(WLED.LED_RR, WLED.WLED_ON)
                    WLED.write(WLED.LED_LL, WLED.WLED_OFF)
                    WLED.write(WLED.LED_FL, WLED.WLED_OFF)
                    WLED.write(WLED.LED_FR, WLED.WLED_OFF)
                    print("RR")
                    time.sleep(2)
                    state = 2

                case 2:
                    WLED.write(WLED.LED_RR, WLED.WLED_OFF)
                    WLED.write(WLED.LED_LL, WLED.WLED_ON)
                    WLED.write(WLED.LED_FL, WLED.WLED_OFF)
                    WLED.write(WLED.LED_FR, WLED.WLED_OFF)
                    print("LL")
                    time.sleep(2)
                    state = 3

                case 3:
                    WLED.write(WLED.LED_RR, WLED.WLED_OFF)
                    WLED.write(WLED.LED_LL, WLED.WLED_OFF)
                    WLED.write(WLED.LED_FL, WLED.WLED_ON)
                    WLED.write(WLED.LED_FR, WLED.WLED_OFF)
                    print("FL")
                    time.sleep(2)
                    state = 4

                case 4:
                    WLED.write(WLED.LED_RR, WLED.WLED_OFF)
                    WLED.write(WLED.LED_LL, WLED.WLED_OFF)
                    WLED.write(WLED.LED_FL, WLED.WLED_OFF)
                    WLED.write(WLED.LED_FR, WLED.WLED_ON)
                    print("FR")
                    time.sleep(2)
                    state = 0
                
                case _:
                    state = 0

    except KeyboardInterrupt :
        print("destruct")
        WLED.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt :
        print("!!Exit!!")
        sys.exit()
