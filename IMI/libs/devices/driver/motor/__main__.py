import sys
from motor import MOTOR
import time

def main():
    motor = MOTOR()
    motor.start()
#    while True:
#        left = input("Left Speed(pps) = ")
#        right = input("Right Speed(pps) = ")
#        input("Press Any Key...")
#        motor.run(int(left), int(right))
#

    motor.run(530, 528)
    time.sleep(0.9*3)
    motor.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt :
        print("!!EXIT!!")
        sys.exit()
