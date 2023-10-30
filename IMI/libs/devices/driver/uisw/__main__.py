import sys
import time
from uisw import *

def main():
    SW = UISW()
    
    while True:
        swst : bool = [False] * 3
        swst[0] = SW.read(UISW.SW0)
        swst[1] = SW.read(UISW.SW1)
        swst[2] = SW.read(UISW.SW2)
        print(swst)
        if swst[0] == True and swst[1] == True and swst[2] == True:
            break;
        time.sleep(1)

if __name__ == "__main__" :
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
