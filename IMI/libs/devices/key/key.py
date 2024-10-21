from logging import ERROR
import sys
import os
from time import sleep, clock_gettime_ns
from enum import Enum, auto
from turtle import rt
import pigpio

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from driver.uisw import uisw as DRV_UISW

class UISWNAME(Enum):
    ESCAPE = 0
    SELECT = 1
    ENTER = 2

class UISWSTATE(Enum):
    NON = auto()        # 押されていない
    PRESS = auto()      # 押した
    PUSH = auto()       # 押して離した
    LONG = auto()       # 押し続けた
    RELEASE = auto()    # 押し続けて離した


class UISWCmd(Enum):
    NON_SW_EVNT     = auto()
    ESC_PUSH        = auto()
    SEL_PUSH        = auto()
    ENT_PUSH        = auto()

    ESC_LONG        = auto()
    SEL_LONG        = auto()
    ENT_LONG        = auto()

    ESC_LRELEASE    = auto()
    SEL_LRELEASE    = auto()
    ENT_LRELEASE    = auto()

    EXIT_PUSH       = auto()
    ERROR           = auto()


class KeyPolling:
    class _SwSt(Enum):
        _INIT       = auto()
        _WAIT_ON  = auto()
        _WAIT_OFF   = auto()
        _WAIT_OFFMASK = auto()
        _WAIT_OFFRELEASE  = auto()

    __cnstcnt : int = 0
    __UISW : DRV_UISW.UISW
    __NZINTV = 0.05
    __LONGTH:int = 3000
    __PUSHTH:int = 200
    __OFFMASK:int = 100
    __esc_raise_time:int
    __sel_raise_time:int
    __ent_raise_time:int

    __esc_high_time:int
    __sel_high_time:int
    __ent_high_time:int

    __esc_fall_time:int
    __sel_fall_time:int
    __ent_fall_time:int
    
    __esc_SwState:_SwSt
    __sel_SwState:_SwSt
    __ent_SwState:_SwSt
    
    

    __esc_fLong:bool
    __sel_fLong:bool
    __ent_fLong:bool

    __esc_foneshot:bool
    __sel_foneshot:bool
    __ent_foneshot:bool
    __ent_fexit:bool

    def __init__(self, pi:pigpio.pi) -> None:
        self.__UISW = DRV_UISW.UISW(pi)
        self.__esc_raise_time = 0
        self.__sel_raise_time = 0
        self.__ent_raise_time = 0
        self.__esc_fall_time = 0
        self.__sel_fall_time = 0
        self.__ent_fall_time = 0
        self.__esc_high_time = 0
        self.__sel_high_time = 0
        self.__ent_high_time = 0

        self.__esc_SwState = self._SwSt._INIT
        self.__sel_SwState = self._SwSt._INIT
        self.__ent_SwState = self._SwSt._INIT

        self.__esc_fLong = False
        self.__sel_fLong = False
        self.__ent_fLong = False
        self.__esc_foneshot = False
        self.__sel_foneshot = False
        self.__ent_foneshot = False
        self.__fexit = False

        self.__cnstcnt += 1
    
    def __del__(self):
        if  self.__cnstcnt > 0:
            self.__UISW.close()
            self.__cnstcnt -= 1
    
    def close(self):
        self.__del__()
    
    def detector(self) -> UISWCmd :
        SWesc1 = self.__UISW.read(self.__UISW.SW0)
        SWsel1 = self.__UISW.read(self.__UISW.SW1)
        SWent1 = self.__UISW.read(self.__UISW.SW2)
        sleep(self.__NZINTV)
        SWesc2 = self.__UISW.read(self.__UISW.SW0)
        SWsel2 = self.__UISW.read(self.__UISW.SW1)
        SWent2 = self.__UISW.read(self.__UISW.SW2)
        now = int(clock_gettime_ns(0) / 1000000)

        if  (SWesc1 == SWesc2) and (SWsel1 == SWsel2) and (SWent2 == SWent2):
            # 状態遷移 INIT 
            # SW2度読み状態が一致している
            SWesc = SWesc1
            SWsel = SWsel1
            SWent = SWent1
            if self.__esc_SwState == self._SwSt._INIT and not SWesc:
                self.__esc_SwState = self._SwSt._WAIT_ON
            # スイッチが押されていると初期化しない
            if self.__sel_SwState == self._SwSt._INIT and not SWsel:
                self.__sel_SwState = self._SwSt._WAIT_ON
            # スイッチが押されていると初期化しない
            if self.__ent_SwState == self._SwSt._INIT and not SWent:
                self.__ent_SwState = self._SwSt._WAIT_ON

            if      self.__esc_SwState == self._SwSt._WAIT_ON and \
                    self.__sel_SwState == self._SwSt._WAIT_ON and \
                    self.__ent_SwState== self._SwSt._WAIT_ON and \
                    SWesc and SWsel and SWent:
                self.__esc_SwState = self._SwSt._INIT
                self.__sel_SwState = self._SwSt._INIT
                self.__ent_SwState = self._SwSt._INIT
                self.__esc_fall_time = now
                self.__sel_fall_time = now
                self.__ent_fall_time = now
                self.__fexit = True
            
            else:
                #  ESCスイッチのONを検出
                if  self.__esc_SwState == self._SwSt._WAIT_ON and SWesc:
                    self.__esc_SwState = self._SwSt._WAIT_OFF
                    self.__esc_raise_time = now

                elif    self.__esc_SwState == self._SwSt._WAIT_OFF and SWesc and \
                        (now - self.__esc_raise_time) > self.__LONGTH:
                    self.__esc_SwState = self._SwSt._WAIT_OFFRELEASE
                    self.__esc_fLong = True
                    self.__esc_foneshot = True

                # ESCスイッチのOFFを検出
                elif (  self.__esc_SwState == self._SwSt._WAIT_OFFRELEASE or \
                        self.__esc_SwState == self._SwSt._WAIT_OFF ) and  \
                        not SWesc:
                    self.__esc_SwState = self._SwSt._WAIT_OFFMASK
                    self.__esc_fall_time= now
                    self.__esc_foneshot = True
                    self.__esc_high_time = now - self.__esc_raise_time

                # ESCスイッチのOFFマスク
                elif    self.__esc_SwState == self._SwSt._WAIT_OFFMASK and not SWesc and \
                        (now - self.__esc_fall_time) > self.__OFFMASK:
                    self.__esc_high_time = 0
                    self.__esc_fLong = False
                    self.__esc_raise_time = now
                    self.__esc_fall_time = now
                    self.__esc_fLong = False
                    self.__esc_SwState = self._SwSt._WAIT_ON

                #  SELスイッチのONを検出
                if  self.__sel_SwState == self._SwSt._WAIT_ON and SWsel:
                    self.__sel_SwState = self._SwSt._WAIT_OFF
                    self.__sel_raise_time = now

                # SELスイッチ長押し判定
                elif    self.__sel_SwState == self._SwSt._WAIT_OFF and SWsel and \
                        (now - self.__sel_raise_time) > self.__LONGTH:
                    self.__sel_SwState = self._SwSt._WAIT_OFFRELEASE
                    self.__sel_fLong = True
                    self.__sel_foneshot = True

                # SELスイッチのOFFを検出
                elif (  self.__sel_SwState == self._SwSt._WAIT_OFFRELEASE or \
                        self.__sel_SwState == self._SwSt._WAIT_OFF ) and  \
                        not SWsel:
                    self.__sel_SwState = self._SwSt._WAIT_OFFMASK
                    self.__sel_fall_time= now
                    self.__sel_foneshot = True
                    self.__sel_high_time = now - self.__sel_raise_time

                # SELスイッチのOFFマスク
                elif    self.__sel_SwState == self._SwSt._WAIT_OFFMASK and not SWsel and \
                        (now - self.__sel_fall_time) > self.__OFFMASK:
                    self.__sel_high_time = 0
                    self.__sel_fLong = False
                    self.__sel_raise_time = now
                    self.__sel_fall_time = now
                    self.__sel_fLong = False
                    self.__sel_SwState = self._SwSt._WAIT_ON

                #  ENTスイッチのONを検出
                if  self.__ent_SwState == self._SwSt._WAIT_ON and SWent:
                    self.__ent_SwState = self._SwSt._WAIT_OFF
                    self.__ent_raise_time = now

                # ENTスイッチ長押し判定
                elif    self.__ent_SwState == self._SwSt._WAIT_OFF and SWent and \
                        (now - self.__ent_raise_time) > self.__LONGTH:
                    self.__ent_SwState = self._SwSt._WAIT_OFFRELEASE
                    self.__ent_fLong = True
                    self.__ent_foneshot = True

                # ENTスイッチのOFFを検出
                elif (  self.__ent_SwState == self._SwSt._WAIT_OFFRELEASE or \
                        self.__ent_SwState == self._SwSt._WAIT_OFF ) and  \
                        not SWent:
                    self.__ent_SwState = self._SwSt._WAIT_OFFMASK
                    self.__ent_fall_time= now
                    self.__ent_foneshot = True
                    self.__ent_high_time = now - self.__ent_raise_time

                # ENTスイッチのOFFマスク
                elif    self.__ent_SwState == self._SwSt._WAIT_OFFMASK and not SWent and \
                        (now - self.__ent_fall_time) > self.__OFFMASK:
                    self.__ent_high_time = 0
                    self.__ent_fLong = False
                    self.__ent_raise_time = now
                    self.__ent_fall_time = now
                    self.__ent_fLong = False
                    self.__ent_SwState = self._SwSt._WAIT_ON

        # 全押し
        if self.__fexit:
            self.__fexit = False
            return UISWCmd.EXIT_PUSH

        elif self.__esc_foneshot:
            # ON->OFF遷移が終わっているのでイベントを発生
            self.__esc_foneshot = False
            if self.__esc_fLong and self.__esc_SwState == self._SwSt._WAIT_OFFRELEASE:
                return UISWCmd.ESC_LONG
            elif self.__esc_fLong and self.__esc_SwState == self._SwSt._WAIT_OFFMASK:
                return UISWCmd.ESC_LRELEASE
            elif  self.__esc_SwState == self._SwSt._WAIT_OFFMASK:
                return UISWCmd.ESC_PUSH
            else:
                return UISWCmd.NON_SW_EVNT
        elif self.__sel_foneshot:
            # ON->OFF遷移が終わっているのでイベントを発生
            self.__sel_foneshot = False
            if self.__sel_fLong and self.__sel_SwState == self._SwSt._WAIT_OFFRELEASE:
                return UISWCmd.SEL_LONG
            elif self.__sel_fLong and self.__sel_SwState == self._SwSt._WAIT_OFFMASK:
                return UISWCmd.SEL_LRELEASE
            elif  self.__sel_SwState == self._SwSt._WAIT_OFFMASK:
                return UISWCmd.SEL_PUSH
            else:
                return UISWCmd.NON_SW_EVNT
        elif self.__ent_foneshot:
            # ON->OFF遷移が終わっているのでイベントを発生
            self.__ent_foneshot = False
            if self.__ent_fLong and self.__ent_SwState == self._SwSt._WAIT_OFFRELEASE:
                return UISWCmd.ENT_LONG
            elif self.__ent_fLong and self.__ent_SwState == self._SwSt._WAIT_OFFMASK:
                return UISWCmd.ENT_LRELEASE
            elif  self.__ent_SwState == self._SwSt._WAIT_OFFMASK:
                return UISWCmd.ENT_PUSH
            else:
                return UISWCmd.NON_SW_EVNT
        else :
            return UISWCmd.NON_SW_EVNT




class KeyEvent:
    class __ExitState(Enum):
        INIT = auto()
        WAIT_PRESS = auto()
        WAIT_RELEASE = auto()

    __KEYPI:pigpio.pi
    __cnstcnt : int = 0
    __UISW : DRV_UISW.UISW
    __NZINTV = 0.05
    __LONGTH:int = 3000000
    __PUSHTH:int = 100000
    __OFFMASK:int = 1000

    __esc_sw_onoff:bool
    __sel_sw_onoff:bool
    __ent_sw_onoff:bool
    __esc_raise_time:int
    __sel_raise_time:int
    __ent_raise_time:int

    __esc_fall_time:int
    __sel_fall_time:int
    __ent_fall_time:int

    __esc_raise_time_bck:int
    __sel_raise_time_bck:int
    __ent_raise_time_bck:int

    __esc_fall_time_bck:int
    __sel_fall_time_bck:int
    __ent_fall_time_bck:int

    __exitStateBF:__ExitState
    __escExitStateBF:UISWSTATE
    __selExitStateBF:UISWSTATE
    __entExitStateBF:UISWSTATE

    def __init__(self, pi:pigpio.pi) -> None:
        self.__KEYPI = pi
        self.__UISW = DRV_UISW.UISW(pi=pi, intrFuncSW0=self._escIntr, intrFuncSW1=self._selIntr, intrFuncSW2=self._entIntr)
        self.__esc_raise_time = 0
        self.__sel_raise_time = 0
        self.__ent_raise_time = 0
        self.__esc_fall_time = 0
        self.__sel_fall_time = 0
        self.__ent_fall_time = 0
        self.__esc_raise_time_bck = 0
        self.__sel_raise_time_bck = 0
        self.__ent_raise_time_bck = 0
        self.__esc_fall_time_bck = 0
        self.__sel_fall_time_bck = 0
        self.__ent_fall_time_bck = 0
        self.__esc_sw_onoff = False
        self.__sel_sw_onoff = False
        self.__ent_sw_onoff = False
        self.__exitStateBF = self.__ExitState.INIT
        self.__escExitStateBF = UISWSTATE.NON
        self.__selExitStateBF = UISWSTATE.NON
        self.__entExitStateBF = UISWSTATE.NON


        self.__cnstcnt += 1
    
    def __del__(self):
        if  self.__cnstcnt > 0:
            self.__UISW.close()
            self.__cnstcnt -= 1
    
    def close(self):
        self.__del__()
    

    def _entIntr(self, pin:int, level:bool, tick:int):
        if level == 0:
            # SW == ON
            self.__ent_sw_onoff = True
            self.__ent_raise_time = tick
        else:
            # SW == OFF
            self.__ent_sw_onoff = False
            self.__ent_fall_time = tick

    def _escIntr(self, pin:int, level:bool, tick:int):
        if level == 0:
            # SW == ON
            self.__esc_sw_onoff = True 
            self.__esc_raise_time = tick
        else:
            # SW == OFF
            self.__esc_sw_onoff = False
            self.__esc_fall_time = tick

    def _selIntr(self, pin:int, level:bool, tick:int):
        if level == 0:
            # SW == ON
            self.__sel_sw_onoff = True 
            self.__sel_raise_time = tick
        else:
            # SW == OFF
            self.__sel_sw_onoff = False
            self.__sel_fall_time = tick
    
    # 通常の制御周期で過去のスイッチエッジ履歴から判定する。判定済みかどうかはこの時点では考えない。
    def __swState(self, onoff:bool, nowT:int,  raiseT:int, raiseLastT:int, fallT:int, fallLastT:int) -> tuple[bool, UISWSTATE, int, int]:
    
        onEdgeTiming = pigpio.tickDiff(raiseT, nowT)
        offEdgeTiming = pigpio.tickDiff(fallT, nowT)
        rtnSwState = UISWSTATE.NON
        updateRaiseT:int = raiseLastT
        updateFallT:int = fallLastT
        if onoff:
            pushT = onEdgeTiming
            # 押されている時間が長い。常にイベントが発生する。
            if pushT > self.__LONGTH:
                rtnSwState = UISWSTATE.LONG
            # 押され始めたなら。一度しかイベントを発生させない
            elif updateRaiseT != raiseT and pushT > self.__PUSHTH:
                updateRaiseT:int = raiseT
                rtnSwState = UISWSTATE.PRESS
            
        # OFF
        else:
            pushT = pigpio.tickDiff(raiseT, fallT)
            if updateFallT != fallT and pushT > self.__LONGTH and offEdgeTiming > self.__OFFMASK:
                rtnSwState = UISWSTATE.RELEASE
                updateFallT:int = fallT
            elif updateFallT != fallT and pushT > self.__PUSHTH and offEdgeTiming > self.__OFFMASK:
                updateFallT:int = fallT
                rtnSwState = UISWSTATE.PUSH
        return (onoff, rtnSwState, updateRaiseT, updateFallT)


    def detector(self) -> tuple[bool, bool, dict[UISWNAME, UISWSTATE]]:
        rtnStDict:dict[UISWNAME, UISWSTATE]
        exitflg:bool = False
        update:bool = False
        
        esconoff, escSwSt,self.__esc_raise_time_bck, self.__esc_fall_time_bck = \
                                            self.__swState( onoff=self.__esc_sw_onoff,
                                                            nowT=self.__KEYPI.get_current_tick(),
                                                            raiseT=self.__esc_raise_time, raiseLastT=self.__esc_raise_time_bck,
                                                            fallT=self.__esc_fall_time, fallLastT=self.__esc_fall_time_bck)

        selonoff, selSwSt,self.__sel_raise_time_bck, self.__sel_fall_time_bck  = \
                                            self.__swState( onoff=self.__sel_sw_onoff,
                                                            nowT=self.__KEYPI.get_current_tick(),
                                                            raiseT=self.__sel_raise_time, raiseLastT=self.__sel_raise_time_bck,
                                                            fallT=self.__sel_fall_time, fallLastT=self.__sel_fall_time_bck)

        entonoff, entSwSt,self.__ent_raise_time_bck, self.__ent_fall_time_bck  = \
                                            self.__swState( onoff=self.__ent_sw_onoff,
                                                            nowT=self.__KEYPI.get_current_tick(),
                                                            raiseT=self.__ent_raise_time, raiseLastT=self.__ent_raise_time_bck,
                                                            fallT=self.__ent_fall_time, fallLastT=self.__ent_fall_time_bck)
        # print(f"{self.__esc_raise_time}/{self.__esc_fall_time}, {self.__sel_raise_time}/{self.__sel_fall_time}, {self.__ent_raise_time}/{self.__ent_fall_time}")
        update = (escSwSt is not UISWSTATE.NON) or (selSwSt is not UISWSTATE.NON) or (entSwSt is not UISWSTATE.NON)
        rtnStDict = {UISWNAME.ESCAPE:escSwSt, UISWNAME.SELECT:selSwSt, UISWNAME.ENTER:entSwSt}
        match self.__exitStateBF:
            case self.__ExitState.INIT:
                if not esconoff and not selonoff and not entonoff:
                    self.__escExitStateBF = UISWSTATE.NON
                    self.__selExitStateBF = UISWSTATE.NON
                    self.__entExitStateBF = UISWSTATE.NON
                    self.__exitStateBF = self.__ExitState.WAIT_PRESS
                    exitflg = False
            case self.__ExitState.WAIT_PRESS:
                if escSwSt == UISWSTATE.PRESS:
                    self.__escExitStateBF = UISWSTATE.PRESS
                elif escSwSt == UISWSTATE.PUSH or escSwSt == UISWSTATE.RELEASE:
                    self.__escExitStateBF = UISWSTATE.RELEASE

                if selSwSt == UISWSTATE.PRESS:
                    self.__selExitStateBF = UISWSTATE.PRESS
                elif selSwSt == UISWSTATE.PUSH or selSwSt == UISWSTATE.RELEASE:
                    self.__selExitStateBF = UISWSTATE.RELEASE

                if entSwSt == UISWSTATE.PRESS:
                    self.__entExitStateBF = UISWSTATE.PRESS
                elif entSwSt == UISWSTATE.PUSH or entSwSt == UISWSTATE.RELEASE:
                    self.__entExitStateBF = UISWSTATE.RELEASE

                if  self.__escExitStateBF == UISWSTATE.PRESS and \
                    self.__selExitStateBF == UISWSTATE.PRESS and \
                    self.__entExitStateBF == UISWSTATE.PRESS:
                    self.__exitStateBF = self.__ExitState.WAIT_RELEASE
                    exitflg = False
            case self.__ExitState.WAIT_RELEASE:
                if escSwSt == UISWSTATE.PUSH or escSwSt == UISWSTATE.RELEASE:
                    self.__escExitStateBF = UISWSTATE.RELEASE
                if selSwSt == UISWSTATE.PUSH or selSwSt == UISWSTATE.RELEASE:
                    self.__selExitStateBF = UISWSTATE.RELEASE
                if entSwSt == UISWSTATE.PUSH or entSwSt == UISWSTATE.RELEASE:
                    self.__entExitStateBF = UISWSTATE.RELEASE

                if  self.__escExitStateBF == UISWSTATE.RELEASE and \
                    self.__selExitStateBF == UISWSTATE.RELEASE and \
                    self.__entExitStateBF == UISWSTATE.RELEASE:
                    exitflg = True 
                    self.__exitStateBF = self.__ExitState.WAIT_PRESS
        return update, exitflg,rtnStDict 




