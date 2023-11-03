import time
import sys
from wallsensors import wallsensors


def main():
    ws = wallsensors()
    cnt = 0
    while True:
        #print(ws.readRaw())
        # print(ws.readNormalized())
        print(f"{cnt},{ws.read()}")
        time.sleep(0.5)
        cnt += 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt :
        print("!!Exit!!")
        sys.exit()

