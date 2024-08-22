import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from .imimessage import IMISensorsDict
from .libs.devices.wallsensors import wallsensors

class IMISensor:
    
    __WALL:wallsensors.wallsensors
    __cnstcnt:int = 0
    def __init__(self) -> None:
        self.__WALL = wallsensors.wallsensors()
        self.__cnstcnt += 1

    def __del__(self):
        if 0 < self.__cnstcnt:
            self.__cnstcnt -= 1

    def close(self):
        self.__del__()

    def read(self, timestanp:int) -> IMISensorsDict:
        wallinfo = self.__WALL.read()
        wval:IMISensorsDict = {
            'timestamp':timestanp,
            'wallflag':(wallinfo[0], wallinfo[1], wallinfo[2]),
            'wallvalue':(wallinfo[3], wallinfo[4],wallinfo[5])
        }
        return wval
