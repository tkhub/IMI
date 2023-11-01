import time
from devices.driver import uiled as ULED

def main():
    led = ULED.UILED()
    led.write(led.UILED0, led.UILED_OFF)
    led.write(led.UILED1, led.UILED_OFF)
    led.write(led.UILED2, led.UILED_OFF)
    led.write(led.UILED3, led.UILED_OFF)
    time.sleep(0.5)
    led.write(led.UILED0, led.UILED_ON)
    time.sleep(0.5)
    led.write(led.UILED1, led.UILED_ON)
    time.sleep(0.5)
    led.write(led.UILED2, led.UILED_ON)
    time.sleep(0.5)
    led.write(led.UILED3, led.UILED_ON)
    led.close()

if __name__ == '__main__':
    main()