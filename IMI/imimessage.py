from token import OP
from typing import TypedDict, Optional
from enum import Enum, auto


class IMISensorsDict(TypedDict):
    timestamp:int
    wallflag:tuple[Optional[bool], Optional[bool], Optional[bool]]
    wallvalue:tuple[Optional[float], Optional[float], Optional[float]]
    
class RunCmd(Enum):
    STOP        = auto()
    HALF_STRAGHT = auto()
    STRAIGHT    = auto()
    LEFT_SPINTURN   = auto()
    RIGHT_SPINTURN  = auto()
    LEFT_TURN   = auto()
    RIGHT_TURN  = auto()
    U_TURN      = auto()
    CALIBRATE   = auto()





