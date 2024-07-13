import time
import sys
from wallsensors import wallsensors


def main():
    ws = wallsensors()
    cnt = 0
    loopnum : int = 16
    while True:
        #print(ws.readRaw())
        # print(ws.readNormalized())
        diff : float = 0
        length : float = 0
        deg : float = 0
        print(ws.read())
        for i in range(loopnum):
            tmp = ws.read()
            wallflg = tmp[:3]
            if (tmp[3] != None):
                diff += tmp[3]
            if (tmp[4] != None):
                length += tmp[4]
            if (tmp[5] != None):
                deg += tmp[5]

        diff = diff / loopnum
        length = length / loopnum
        deg = deg / loopnum
        print(f"{cnt},{wallflg}, {diff}, {length}, {deg}")
        time.sleep(0.5)
        cnt += 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt :
        print("!!Exit!!")
        sys.exit()

