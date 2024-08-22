import os, sys
from enum import Enum, auto
from typing import Optional
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from .imimessage import IMISensorsDict, RunCmd
from .libs.devices.wallsensors import wallsensors
from .libs.devices.key.key import UISWCmd

# 与えられた周辺情報から動作を決める

cnt = 0
test_runlist = [RunCmd.HALF_STRAGHT, RunCmd.STRAIGHT, RunCmd.RIGHT_TURN, RunCmd.RIGHT_TURN, RunCmd.STRAIGHT, RunCmd.STRAIGHT, RunCmd.STOP]
class RunMode(Enum):
    SUSPEND = auto()
    RUN = auto()
    NOP = auto()
RunModeSq:RunMode = RunMode.NOP

    
def IMICommander(timestamp:int, wallflag:tuple[Optional[bool], Optional[bool], Optional[bool]] = (None, None, None), wallvalue:tuple[Optional[float], Optional[float], Optional[float]] = (None, None, None)) -> RunCmd:
    global cnt, test_runlist, RunModeSq
    rtncmd:RunCmd = RunCmd.STOP
    if RunModeSq == RunMode.RUN:
        # if wallflag[2] == False:
        #     print("LEFT")
        #     rtncmd = RunCmd.LEFT_TURN
        # elif wallflag[1] == False:
        #     print("STRAIGHT")
        #     rtncmd = RunCmd.STRAIGHT
        # elif wallflag[0] == False:
        #     print("RIGHT")
        #     rtncmd = RunCmd.RIGHT_TURN
        # elif wallflag[0] == True and wallflag[1] == True and wallflag[2] == True:
        #     print("UTURN")
        #     rtncmd = RunCmd.U_TURN
        # else:
        #     pass
        rtncmd = test_runlist[cnt]
        print(f"          rtncmd = {rtncmd}")
        cnt += 1
        if cnt > len(test_runlist):
            cnt = len(test_runlist)
    return rtncmd


def IMIModeChoice(uisw:UISWCmd) -> RunMode:
    global RunModeSq, cnt
    if uisw == UISWCmd.ENT_PUSH:
        print("Choice is Run")
        RunModeSq = RunMode.RUN
    elif uisw == UISWCmd.ESC_PUSH:
        print("Choice is ESC")
        cnt = 0
        RunModeSq = RunMode.SUSPEND
    else:
        pass
    return RunModeSq
