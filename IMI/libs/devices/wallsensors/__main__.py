import time
import sys
from wallsensors import wallsensors
import pigpio


def main():
    pi = pigpio.pi()
    ws = wallsensors(pi)
    cnt = 0
    loopnum : int = 16
    while True:
        #print(ws.readRaw())
        # print(ws.readNormalized())
        diff : float = 0
        length : float = 0
        deg : float = 0
        raw = ws.read()
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
        print(f"{raw}:{cnt},{wallflg}, {diff}, {length}, {deg}")
        time.sleep(0.5)
        cnt += 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt :
        print("!!Exit!!")
        sys.exit()

