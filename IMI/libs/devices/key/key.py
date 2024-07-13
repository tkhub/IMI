import sys
import os
from time import sleep, clock_gettime_ns
from enum import Enum, auto

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from driver.uisw import uisw as DRV_UISW

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


class Key:
    class _SwSt(Enum):
        _INIT       = auto()
        _WAIT_HIGH  = auto()
        _WAIT_LOW   = auto()
        _WAIT_LMASK = auto()
        _WAIT_LRLS  = auto()

    __cnstcnt : int = 0
    __UISW : DRV_UISW
    __NZINTV = 0.01
    __LONGTH:int = 3000
    __PUSHTH:int = 200
    __OFFMASK:int = 200
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

    def __init__(self) -> None:
        self.__UISW = DRV_UISW.UISW()
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
                self.__esc_SwState = self._SwSt._WAIT_HIGH
            # スイッチが押されていると初期化しない
            if self.__sel_SwState == self._SwSt._INIT and not SWsel:
                self.__sel_SwState = self._SwSt._WAIT_HIGH
            # スイッチが押されていると初期化しない
            if self.__ent_SwState == self._SwSt._INIT and not SWent:
                self.__ent_SwState = self._SwSt._WAIT_HIGH

            if      self.__esc_SwState == self._SwSt._WAIT_HIGH and \
                    self.__sel_SwState == self._SwSt._WAIT_HIGH and \
                    self.__ent_SwState== self._SwSt._WAIT_HIGH and \
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
                if  self.__esc_SwState == self._SwSt._WAIT_HIGH and SWesc:
                    self.__esc_SwState = self._SwSt._WAIT_LOW
                    self.__esc_raise_time = now

                elif    self.__esc_SwState == self._SwSt._WAIT_LOW and SWesc and \
                        (now - self.__esc_raise_time) > self.__LONGTH:
                    self.__esc_SwState = self._SwSt._WAIT_LRLS
                    self.__esc_fLong = True
                    self.__esc_foneshot = True

                # ESCスイッチのOFFを検出
                elif (  self.__esc_SwState == self._SwSt._WAIT_LRLS or \
                        self.__esc_SwState == self._SwSt._WAIT_LOW ) and  \
                        not SWesc:
                    self.__esc_SwState = self._SwSt._WAIT_LMASK
                    self.__esc_fall_time= now
                    self.__esc_foneshot = True
                    self.__esc_high_time = now - self.__esc_raise_time

                # ESCスイッチのOFFマスク
                elif    self.__esc_SwState == self._SwSt._WAIT_LMASK and not SWesc and \
                        (now - self.__esc_fall_time) > self.__OFFMASK:
                    self.__esc_high_time = 0
                    self.__esc_fLong = False
                    self.__esc_raise_time = now
                    self.__esc_fall_time = now
                    self.__esc_fLong = False
                    self.__esc_SwState = self._SwSt._WAIT_HIGH

                #  SELスイッチのONを検出
                if  self.__sel_SwState == self._SwSt._WAIT_HIGH and SWsel:
                    self.__sel_SwState = self._SwSt._WAIT_LOW
                    self.__sel_raise_time = now

                # SELスイッチ長押し判定
                elif    self.__sel_SwState == self._SwSt._WAIT_LOW and SWsel and \
                        (now - self.__sel_raise_time) > self.__LONGTH:
                    self.__sel_SwState = self._SwSt._WAIT_LRLS
                    self.__sel_fLong = True
                    self.__sel_foneshot = True

                # SELスイッチのOFFを検出
                elif (  self.__sel_SwState == self._SwSt._WAIT_LRLS or \
                        self.__sel_SwState == self._SwSt._WAIT_LOW ) and  \
                        not SWsel:
                    self.__sel_SwState = self._SwSt._WAIT_LMASK
                    self.__sel_fall_time= now
                    self.__sel_foneshot = True
                    self.__sel_high_time = now - self.__sel_raise_time

                # SELスイッチのOFFマスク
                elif    self.__sel_SwState == self._SwSt._WAIT_LMASK and not SWsel and \
                        (now - self.__sel_fall_time) > self.__OFFMASK:
                    self.__sel_high_time = 0
                    self.__sel_fLong = False
                    self.__sel_raise_time = now
                    self.__sel_fall_time = now
                    self.__sel_fLong = False
                    self.__sel_SwState = self._SwSt._WAIT_HIGH

                #  ENTスイッチのONを検出
                if  self.__ent_SwState == self._SwSt._WAIT_HIGH and SWent:
                    self.__ent_SwState = self._SwSt._WAIT_LOW
                    self.__ent_raise_time = now

                # ENTスイッチ長押し判定
                elif    self.__ent_SwState == self._SwSt._WAIT_LOW and SWent and \
                        (now - self.__ent_raise_time) > self.__LONGTH:
                    self.__ent_SwState = self._SwSt._WAIT_LRLS
                    self.__ent_fLong = True
                    self.__ent_foneshot = True

                # ENTスイッチのOFFを検出
                elif (  self.__ent_SwState == self._SwSt._WAIT_LRLS or \
                        self.__ent_SwState == self._SwSt._WAIT_LOW ) and  \
                        not SWent:
                    self.__ent_SwState = self._SwSt._WAIT_LMASK
                    self.__ent_fall_time= now
                    self.__ent_foneshot = True
                    self.__ent_high_time = now - self.__ent_raise_time

                # ENTスイッチのOFFマスク
                elif    self.__ent_SwState == self._SwSt._WAIT_LMASK and not SWent and \
                        (now - self.__ent_fall_time) > self.__OFFMASK:
                    self.__ent_high_time = 0
                    self.__ent_fLong = False
                    self.__ent_raise_time = now
                    self.__ent_fall_time = now
                    self.__ent_fLong = False
                    self.__ent_SwState = self._SwSt._WAIT_HIGH

        # 全押し
        if self.__fexit:
            self.__fexit = False
            return UISWCmd.EXIT_PUSH

        elif self.__esc_foneshot:
            # ON->OFF遷移が終わっているのでイベントを発生
            self.__esc_foneshot = False
            if self.__esc_fLong and self.__esc_SwState == self._SwSt._WAIT_LRLS:
                return UISWCmd.ESC_LONG
            elif self.__esc_fLong and self.__esc_SwState == self._SwSt._WAIT_LMASK:
                return UISWCmd.ESC_LRELEASE
            elif  self.__esc_SwState == self._SwSt._WAIT_LMASK:
                return UISWCmd.ESC_PUSH
            else:
                return UISWCmd.NON_SW_EVNT
        elif self.__sel_foneshot:
            # ON->OFF遷移が終わっているのでイベントを発生
            self.__sel_foneshot = False
            if self.__sel_fLong and self.__sel_SwState == self._SwSt._WAIT_LRLS:
                return UISWCmd.SEL_LONG
            elif self.__sel_fLong and self.__sel_SwState == self._SwSt._WAIT_LMASK:
                return UISWCmd.SEL_LRELEASE
            elif  self.__sel_SwState == self._SwSt._WAIT_LMASK:
                return UISWCmd.SEL_PUSH
            else:
                return UISWCmd.NON_SW_EVNT
        elif self.__ent_foneshot:
            # ON->OFF遷移が終わっているのでイベントを発生
            self.__ent_foneshot = False
            if self.__ent_fLong and self.__ent_SwState == self._SwSt._WAIT_LRLS:
                return UISWCmd.ENT_LONG
            elif self.__ent_fLong and self.__ent_SwState == self._SwSt._WAIT_LMASK:
                return UISWCmd.ENT_LRELEASE
            elif  self.__ent_SwState == self._SwSt._WAIT_LMASK:
                return UISWCmd.ENT_PUSH
            else:
                return UISWCmd.NON_SW_EVNT
        else :
            return UISWCmd.NON_SW_EVNT



