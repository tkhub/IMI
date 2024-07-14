from enum import Enum, auto

# 与えられた周辺情報から動作を決める

class RunCmd(Enum):
    STOP = auto()
    STRAIGHT = auto()
    LEFT_TURN = auto()
    RIGHT_TURN = auto()
    U_TURN = auto()


