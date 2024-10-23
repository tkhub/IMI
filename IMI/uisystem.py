from distutils.cygwinccompiler import CONFIG_H_NOTOK
from enum import Enum, auto
from imp import SEARCH_ERROR
from logging import ERROR, root
from re import escape
from time import clock_gettime, sleep
from token import OP
from typing import Optional


from .libs.devices.driver.buzzer.buzzer import UIBZ as DRV_BUZZER
from .libs.devices.key.key import UISWNAME, UISWSTATE, UISWEXIT
from .imimessage import JOB, JOB_ARGN, JOB_STATE, JOB_STR, JOB_TABLE, ExecJob
from .imimessage import SoundPattern, SoundPatternTABLE

import pigpio
import busio
import board
from PIL import Image, ImageDraw,ImageFont
import adafruit_ssd1306

#          

class JobControler:
    
    __NOWJOB:JOB = JOB.ERROR
    __OLDJOB:JOB = JOB.ERROR
    __longf:bool
    __cnstcnt:int = 0
    __jobselcnt:int
    __argn:int
    __exec:bool
    def __init__(self) -> None:
        self.__jobselcnt = 0
        self.__cnstcnt += 1
        self.__argn = 0
        self.__longf = False
        self.__exec = False

    def __del__(self):
        self.__cnstcnt -= 1
    
    def close(self):
        self.__del__()

    def __Job2Str(self, job:JOB, argn:int) -> str:
        rtnstr = JOB_STR[job]
        if len(JOB_TABLE[job]) == 2:
            # 続きがない
            rtnstr += " : " + str(argn) + ";"
        else:
            # 続きがある
            for i, j in enumerate(JOB_TABLE[job]):
                if i != 0:
                    if (i - 1) == self.__jobselcnt:
                        rtnstr += ' [' + str(i - 1) + ':' + JOB_STR[j] + ']'
                    else:
                        rtnstr += ' ' + str(i - 1) + ':' + JOB_STR[j]
            rtnstr += ";"
        return rtnstr

    def Selector(self, updatef:bool, exitSt:UISWEXIT, keys:dict[UISWNAME, UISWSTATE]) -> tuple[JOB_STATE, Optional[ExecJob], Optional[str], Optional[SoundPattern]]:
        joblist:list[JOB]
        prev_j:JOB
        next_js:list[JOB]
        soundp:Optional[SoundPattern] = None
        job:Optional[JOB] = None
        jobSt:JOB_STATE = JOB_STATE.INIT
        outstr:Optional[str] = None
        strUpdate:bool = False
        ejob:Optional[ExecJob] = None
        if self.__NOWJOB == JOB.ERROR:
            self.__NOWJOB = JOB.ROOT
            self.__OLDJOB = JOB.ROOT
            self.__longf = False
            soundp = SoundPattern.BOOT_0
            strUpdate = True
            jobSt = JOB_STATE.CHOICE
            update = True
        elif exitSt == UISWEXIT.CONFIRM:
            jobSt = JOB_STATE.ABORT
            soundp = SoundPattern.ABORT
            print("ABORT")
        elif exitSt == UISWEXIT.READY:
            soundp = SoundPattern.ABORT_R
            print("ABORT RADEY")
        elif updatef:
            joblist = JOB_TABLE[self.__NOWJOB]
            prev_j = joblist[0]
            next_js = joblist[1:]
            # 実行中の場合
            if self.__exec:
                # 実行中ESCを押されたら抜ける
                if keys[UISWNAME.ESCAPE] == UISWSTATE.RELEASE:
                    self.__exec = False
                    soundp = SoundPattern.EXIT_0
                    strUpdate = True
                elif keys[UISWNAME.ESCAPE] == UISWSTATE.PRESS:
                    soundp = SoundPattern.CANCEL_0
                    self.__longf = False
                elif keys[UISWNAME.ESCAPE] == UISWSTATE.LONG:
                    if not self.__longf:
                        soundp = SoundPattern.CANCEL_L
                        self.__longf = True
            # 最終端
            elif self.__NOWJOB == next_js[0]:
                # 実行へ移る
                if keys[UISWNAME.ENTER] == UISWSTATE.RELEASE:
                    self.__exec = True
                    ejob = ExecJob()
                    ejob.Job =self.__NOWJOB
                    ejob.Argn = self.__argn
                    soundp = SoundPattern.OK_1
                    strUpdate = True
                elif keys[UISWNAME.ENTER] == UISWSTATE.PRESS:
                    self.__longf = False
                    soundp = SoundPattern.OK_0
                elif keys[UISWNAME.ENTER] == UISWSTATE.LONG:
                    if not self.__longf:
                        soundp = SoundPattern.OK_L
                        self.__longf = True
                # 戻る
                elif keys[UISWNAME.ESCAPE] == UISWSTATE.PUSH:
                    self.__NOWJOB = prev_j
                    soundp = SoundPattern.CANCEL_0
                    self.__jobselcnt = 0
                    strUpdate = True
                elif keys[UISWNAME.SELECT] == UISWSTATE.PUSH:
                    self.__argn += 1
                    self.__argn %= JOB_ARGN[self.__NOWJOB]
                    soundp = SoundPattern.SELECT_0
                    strUpdate = True
            # 最始端
            elif self.__NOWJOB == JOB.ROOT:
                self.__argn = 0
                # 最始端の場合戻れないのでエラー
                if keys[UISWNAME.ESCAPE] == UISWSTATE.PUSH:
                    soundp = SoundPattern.ERROR_0
                elif keys[UISWNAME.ESCAPE] == UISWSTATE.PRESS:
                    soundp = SoundPattern.HALT_R
                elif keys[UISWNAME.ESCAPE] == UISWSTATE.RELEASE:
                    soundp = SoundPattern.HALT
                    jobSt = JOB_STATE.HALT
                elif keys[UISWNAME.ENTER] == UISWSTATE.PUSH:
                    self.__NOWJOB = next_js[self.__jobselcnt]
                    soundp = SoundPattern.OK_0
                    self.__jobselcnt = 0
                    strUpdate = True
                elif keys[UISWNAME.SELECT] == UISWSTATE.PUSH:
                    self.__jobselcnt += 1
                    self.__jobselcnt %= len(next_js)
                    soundp = SoundPattern.SELECT_0
                    strUpdate = True
            else:
                self.__argn = 0
                # 戻る
                if keys[UISWNAME.ESCAPE] == UISWSTATE.PUSH:
                    self.__NOWJOB = prev_j
                    self.__jobselcnt = 0
                    soundp = SoundPattern.CANCEL_0
                    strUpdate = True
                # 入る
                elif keys[UISWNAME.ENTER] == UISWSTATE.PUSH:
                    self.__NOWJOB = next_js[self.__jobselcnt]
                    self.__jobselcnt = 0
                    soundp = SoundPattern.OK_0
                    strUpdate = True
                # 選ぶ
                elif keys[UISWNAME.SELECT] == UISWSTATE.PUSH:
                    self.__jobselcnt += 1
                    self.__jobselcnt %= len(next_js)
                    soundp = SoundPattern.SELECT_0
                    strUpdate = True
            
        if strUpdate:
            outstr = self.__Job2Str(self.__NOWJOB, self.__argn)
            # print(f'{outstr}, {escape}')
        return (jobSt, ejob, outstr, soundp )
    
    def nantyarakantyara(self):
        pass
        

class DisplayControler:
    __cntstcnt:int = 0
    __I2C:busio.I2C
    __DSP:adafruit_ssd1306.SSD1306_I2C
    # __IMGBF
    __WIDTH:int
    __HIGHT:int
    def __init__(self, address:int, displaysize_width_height:tuple[int, int]) -> None:
        self.__I2C = busio.I2C(board.SCL, board.SDA)
        self.__DSP = adafruit_ssd1306.SSD1306_I2C(displaysize_width_height[0], displaysize_width_height[1], self.__I2C, addr=address)
        self.__IMGBF = Image.new("1", displaysize_width_height)
        self.__WIDTH = displaysize_width_height[0]
        self.__HIGHT = displaysize_width_height[1]
        self.__FONT = ImageFont.load_default()
        self.__DSP.fill(1)
        self.__DSP.show()
        self.__cntstcnt += 1
        sleep(0.5)
    
    def __del__(self):
        if self.__cntstcnt > 0:
            self.screenoff()
            self.__cntstcnt -= 1

    def close(self):
        self.__del__()

    def __getTextSize(self, text:str) -> tuple[int, int]:
        left, top, right, bottom = self.__FONT.getbbox(text)
        return (int(right - left), int(bottom - top))

    def exitmesg(self, normal:bool) -> None:
        mesg:str
        if normal:
            mesg = "Go Next!"
        else:
            mesg = "exit..."
        draw = ImageDraw.Draw(self.__IMGBF)
        draw.rectangle((1,1, self.__WIDTH -1, self.__HIGHT - 1), outline=255, fill=255)
        (font_width, font_height) = self.__getTextSize(mesg)
        draw.text((self.__WIDTH // 2 - font_width // 2, self.__HIGHT // 2 - font_height // 2), mesg, font=self.__FONT, fill=0)
        self.__DSP.image(self.__IMGBF)
        self.__DSP.show()

    def bootmesg(self):
        Rectangle_H = [64, 64]
        draw = ImageDraw.Draw(self.__IMGBF)
        draw.rectangle((self.__WIDTH // 2 - Rectangle_H[0] // 2, self.__HIGHT // 2 - Rectangle_H[1] // 2, \
                        self.__WIDTH // 2 + Rectangle_H[0] // 2, self.__HIGHT // 2 + Rectangle_H[1] // 2), outline=255, fill=0)
        
        print(draw)
        print(self.__IMGBF)
        self.__DSP.image(self.__IMGBF)
        self.__DSP.show()

    def screenoff(self):
        self.__DSP.fill(1)
        self.__DSP.show()
        sleep(1)
        self.__DSP.fill(0)
        self.__DSP.show()


class Sound:
    __cnstcnt : int = 0
    __UIBZ : DRV_BUZZER

    def __init__(self, pi:pigpio.pi) -> None:
        self.__UIBZ = DRV_BUZZER(pi)
        self.__cnstcnt += 1
    
    def __del__(self):
        self.__UIBZ.close()
        self.__cnstcnt -= 1
    
    def close(self):
        self.__del__()
    
    def play(self, soundP:SoundPattern) -> None:

        if soundP in SoundPatternTABLE:
            for frq, play, stop in SoundPatternTABLE[soundP]:
                if frq is None:
                    pass
                else:
                    self.__UIBZ.play(freq=frq, playLength=play, pauseLength=stop)
        else:
            print("Out of Table")