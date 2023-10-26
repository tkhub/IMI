import sys
from motor import MOTOR

def main():
    motor = MOTOR()
    motor.start()
    while True:
        left = input("Left Speed(pps) = ")
        right = input("Right Speed(pps) = ")
        input("Press Any Key...")
        motor.run(int(left), int(right))

    motor.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt :
        print("!!EXIT!!")
        sys.exit()
