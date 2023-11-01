import sys
from motion import *
import time

def main():
    mti= motion()
    mti.start()
    while True:
        # ユースケース1：超信地旋回 speed = 0, deg = x time = x
        # ユースケース2-1：スラローム speed = x, deg = x time = x
        # ユースケース2-2：直線 speed = x, deg = x length = x
        speed = input("Speed[mm/s] = ")
        if speed == str(''):
            speed = None
        elif speed != None:
            speed = float(speed)
        degrees = input("Degrees = ")
        if degrees == str(''):
            degrees = None
        elif degrees != None:
            degrees = float(degrees)
        time = input("opt. time[sec] = ")
        if time == str(''):
            time = None
        elif time != None:
            time = float(time)
        length = input("length. time[mm] = ")
        if length == str(''):
            length = None
        elif length!= None:
            length = float(length)
        input("Press Any Key...")
        print(mti.run(speed_mmps=speed, degrees=degrees, runTime=time, length=length,continueFlag=False))
        if degrees == None:
            print("Exit")
            break;
    mti.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt :
        print("!!EXIT!!")
        sys.exit()
