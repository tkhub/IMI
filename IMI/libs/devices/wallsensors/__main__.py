import time
import sys
from wallsensors import wallsensors


def main():
    ws = wallsensors()
    cmd = 'a'
    while True:
        # time.sleep(0.5)
        # cmd = input("ch > ")
        # if cmd == 'q':
        #     break
        # elif cmd == '0' or cmd == '1' or cmd == '2' or cmd == '3' or cmd == '4' or cmd == '5':
        #     print(cmd)
        #     print(type(cmd))
        #     print(ws._testRead(int(cmd)))
        # else:
        print(ws.readRaw())
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt :
        print("!!Exit!!")
        sys.exit()

