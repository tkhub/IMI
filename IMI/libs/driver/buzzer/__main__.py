import time
import sys
from buzzer import UIBZ

def main():
    BZ = UIBZ()
    BZ.play(261)
    time.sleep(1)
    BZ.play(293, 0.5)
    time.sleep(1)
    BZ.play(329, 0.5,0.5)
    BZ.play(391, 0.5)

if __name__ == '__main__':
    main()
