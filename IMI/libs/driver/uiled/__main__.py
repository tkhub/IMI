import sys
import time
from uiled import UILED

def main():
    LED = UILED()
    state:int = 0
    while True:
        match state:
            case 0:
                LED.write(LED.UILED0, LED.UILED_OFF)
                LED.write(LED.UILED1, LED.UILED_OFF)
                LED.write(LED.UILED2, LED.UILED_OFF)
                LED.write(LED.UILED3, LED.UILED_OFF)
                state = 1

            case 1:
                LED.write(LED.UILED0, LED.UILED_ON)
                state = 2

            case 2:
                LED.write(LED.UILED1, LED.UILED_ON)
                state = 3

            case 3:
                LED.write(LED.UILED2, LED.UILED_ON)
                state = 4

            case 4:
                LED.write(LED.UILED3, LED.UILED_ON)
                state = 0
            
            case _:
                state = 0

        time.sleep(0.5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt :
        print("!!Exit!!")
        sys.exit()
