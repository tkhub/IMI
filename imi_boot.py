import sys
from time import time, sleep
from datetime import datetime
from typing import Optional

import netifaces
import busio
import board
from PIL import Image, ImageDraw,ImageFont
import adafruit_ssd1306

import pigpio

IMISW0_PIN = 20
IMISW1_PIN = 26
IMISW2_PIN = 21

IMILED3_PIN = 18
IMILED2_PIN = 23
IMILED1_PIN = 24
IMILED0_PIN = 25

SOUND_PIN = 19

def lanip_getstr(ifname:str) -> str:
    iflist = netifaces.interfaces()
    if ifname not in iflist:
        return "NO I/F"
    else:
        address = netifaces.ifaddresses(ifname)
        if netifaces.AF_INET not in address.keys():
            return "No Connection" 
        else:
            if 'addr' not in address[netifaces.AF_INET][0].keys():
                return "No Connection" 
            else:
                return address[netifaces.AF_INET][0]['addr']
    # Not Reaceable
    return ""

class Display:

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

    def bootmesg(self, hostname:str, eth:str, wlan:str):
        now:datetime = datetime.now()

        draw = ImageDraw.Draw(self.__IMGBF)
        draw.rectangle((1,1, self.__WIDTH -1, self.__HIGHT - 1), outline=255, fill=255)
        ## System name, date, hostname, eth0 ip, wlan0 ip, buttons
        msg = [ "#### IMI3 ####", 
                now.strftime('%Y/%m/%d %H:%M:%S'),
                "hostname:" + hostname,
                "eth0: " + eth,
                "wlan0: " + wlan,
                "sw0 + sw1 + sw2"]
        tabspace:int = 4
        linespace:int = 1
        lineheight:int = linespace
        for index, linstr in enumerate(msg):
            (font_width, font_height) = self.__getTextSize(msg[index])
            draw.text((4, lineheight), msg[index], font=self.__FONT, fill=0)
            lineheight += font_height + linespace
        self.__DSP.image(self.__IMGBF)
        self.__DSP.show()
        # draw.rectangle((1,1, self.__WIDTH -1, self.__HIGHT - 1), outline=255, fill=255)
        
        # draw.rectangle(())
    def screenoff(self):
        self.__DSP.fill(1)
        self.__DSP.show()
        sleep(1)
        self.__DSP.fill(0)
        self.__DSP.show()


def main() -> bool:
    bootst:bool = False
    SOUND_STOPDT = 255
    SOUND_PLAYDT = 128
    SOUND_HTONE = 1760
    SOUND_MIDTONE = 660
    SOUND_LOWTONE = 220
    I2C_ADDR = 0x3C
    displaysize:tuple[int, int] = (128,64)
    pi = pigpio.pi()
    pi.set_mode(IMISW0_PIN, pigpio.INPUT)
    pi.set_mode(IMISW1_PIN, pigpio.INPUT)
    pi.set_mode(IMISW2_PIN, pigpio.INPUT)
    pi.set_pull_up_down(IMISW0_PIN, pigpio.PUD_UP)
    pi.set_pull_up_down(IMISW1_PIN, pigpio.PUD_UP)
    pi.set_pull_up_down(IMISW2_PIN, pigpio.PUD_UP)
    pi.set_mode(IMILED0_PIN, pigpio.OUTPUT)
    pi.set_mode(IMILED1_PIN, pigpio.OUTPUT)
    pi.set_mode(IMILED2_PIN, pigpio.OUTPUT)
    pi.set_mode(IMILED3_PIN, pigpio.OUTPUT)
    pi.write(IMILED0_PIN, pigpio.LOW)
    pi.write(IMILED1_PIN, pigpio.LOW)
    pi.write(IMILED2_PIN, pigpio.LOW)
    pi.write(IMILED3_PIN, pigpio.LOW)
    oled = Display(address=I2C_ADDR, displaysize_width_height=displaysize)
    oled.bootmesg("rpmouse.local", lanip_getstr('eth0'), lanip_getstr('wlan0'))
    pi.set_PWM_dutycycle(SOUND_PIN, SOUND_PLAYDT)
    pi.set_PWM_frequency(SOUND_PIN, SOUND_LOWTONE)
    sleep(0.25)
    pi.set_PWM_frequency(SOUND_PIN, SOUND_MIDTONE)
    sleep(0.25)
    pi.set_PWM_frequency(SOUND_PIN, SOUND_HTONE)
    pi.set_PWM_dutycycle(SOUND_PIN, SOUND_STOPDT)
    imisw0:bool
    imisw1:bool
    imisw2:bool
    cnt:int = 0
    screenOffIntv:int = 20
    screenUpdateTime:float = time()
    f_screenOn:bool = True
    while True:
        imisw0 = bool(pi.read(IMISW0_PIN))
        imisw1 = bool(pi.read(IMISW1_PIN))
        imisw2 = bool(pi.read(IMISW2_PIN))
        sleep(0.05)
        if int(time() - screenUpdateTime) > screenOffIntv:
            if f_screenOn:
                oled.screenoff()
                f_screenOn = False

        if      (not f_screenOn) and \
                ((not imisw0 and imisw1 and imisw2) or \
                (imisw0 and not imisw1 and imisw2) or \
                (imisw0 and imisw1 and not imisw2)):
            oled.bootmesg("rpmouse.local", lanip_getstr('eth0'), lanip_getstr('wlan0'))
            f_screenOn = True
            screenUpdateTime = time()
            pi.set_PWM_dutycycle(SOUND_PIN, SOUND_PLAYDT)
            pi.set_PWM_frequency(SOUND_PIN, SOUND_MIDTONE)
            sleep(0.1)
            pi.set_PWM_dutycycle(SOUND_PIN, SOUND_STOPDT)
        elif    (f_screenOn) and \
                (not imisw0 and imisw1 and not imisw2):
            oled.exitmesg(True)
            pi.set_PWM_dutycycle(SOUND_PIN, SOUND_PLAYDT)
            pi.set_PWM_frequency(SOUND_PIN, SOUND_LOWTONE)
            sleep(0.1)
            pi.set_PWM_frequency(SOUND_PIN, SOUND_MIDTONE)
            pi.write(IMILED0_PIN, pigpio.HIGH)
            pi.write(IMILED1_PIN, pigpio.LOW)
            pi.write(IMILED2_PIN, pigpio.LOW)
            pi.write(IMILED3_PIN, pigpio.LOW)
            sleep(0.1)
            pi.set_PWM_frequency(SOUND_PIN, SOUND_HTONE)
            pi.write(IMILED0_PIN, pigpio.LOW)
            pi.write(IMILED1_PIN, pigpio.HIGH)
            pi.write(IMILED2_PIN, pigpio.LOW)
            pi.write(IMILED3_PIN, pigpio.LOW)
            sleep(0.1)
            pi.set_PWM_frequency(SOUND_PIN, SOUND_LOWTONE)
            pi.write(IMILED0_PIN, pigpio.LOW)
            pi.write(IMILED1_PIN, pigpio.LOW)
            pi.write(IMILED2_PIN, pigpio.HIGH)
            pi.write(IMILED3_PIN, pigpio.LOW)
            sleep(0.1)
            pi.set_PWM_frequency(SOUND_PIN, SOUND_MIDTONE)
            pi.write(IMILED0_PIN, pigpio.LOW)
            pi.write(IMILED1_PIN, pigpio.LOW)
            pi.write(IMILED2_PIN, pigpio.LOW)
            pi.write(IMILED3_PIN, pigpio.HIGH)
            sleep(0.1)
            pi.set_PWM_frequency(SOUND_PIN, SOUND_HTONE)
            pi.write(IMILED0_PIN, pigpio.LOW)
            pi.write(IMILED1_PIN, pigpio.LOW)
            pi.write(IMILED2_PIN, pigpio.LOW)
            pi.write(IMILED3_PIN, pigpio.LOW)
            sleep(0.1)
            pi.set_PWM_dutycycle(SOUND_PIN, SOUND_STOPDT)
            oled.screenoff()
            bootst = True
            break

        elif not imisw0 and not imisw1 and not imisw2:
            oled.exitmesg(False)
            pi.set_PWM_dutycycle(SOUND_PIN, SOUND_PLAYDT)
            pi.set_PWM_frequency(SOUND_PIN, SOUND_HTONE)
            sleep(0.1)
            pi.write(IMILED0_PIN, pigpio.HIGH)
            pi.write(IMILED1_PIN, pigpio.HIGH)
            pi.write(IMILED2_PIN, pigpio.HIGH)
            pi.write(IMILED3_PIN, pigpio.HIGH)
            sleep(0.05)
            pi.set_PWM_frequency(SOUND_PIN, SOUND_LOWTONE)
            pi.write(IMILED0_PIN, pigpio.LOW)
            pi.write(IMILED1_PIN, pigpio.LOW)
            pi.write(IMILED2_PIN, pigpio.LOW)
            pi.write(IMILED3_PIN, pigpio.LOW)
            sleep(0.1)
            pi.write(IMILED0_PIN, pigpio.HIGH)
            pi.write(IMILED1_PIN, pigpio.HIGH)
            pi.write(IMILED2_PIN, pigpio.HIGH)
            pi.write(IMILED3_PIN, pigpio.HIGH)
            sleep(0.05)
            pi.set_PWM_frequency(SOUND_PIN, SOUND_HTONE)
            pi.write(IMILED0_PIN, pigpio.LOW)
            pi.write(IMILED1_PIN, pigpio.LOW)
            pi.write(IMILED2_PIN, pigpio.LOW)
            pi.write(IMILED3_PIN, pigpio.LOW)
            sleep(0.1)
            pi.write(IMILED0_PIN, pigpio.HIGH)
            pi.write(IMILED1_PIN, pigpio.HIGH)
            pi.write(IMILED2_PIN, pigpio.HIGH)
            pi.write(IMILED3_PIN, pigpio.HIGH)
            sleep(0.05)
            pi.set_PWM_frequency(SOUND_PIN, SOUND_LOWTONE)
            pi.write(IMILED0_PIN, pigpio.LOW)
            pi.write(IMILED1_PIN, pigpio.LOW)
            pi.write(IMILED2_PIN, pigpio.LOW)
            pi.write(IMILED3_PIN, pigpio.LOW)
            sleep(0.1)
            pi.set_PWM_dutycycle(SOUND_PIN, SOUND_STOPDT)
            oled.screenoff()
            bootst = False
            break
    while True:
        imisw0 = bool(pi.read(IMISW0_PIN))
        imisw1 = bool(pi.read(IMISW1_PIN))
        imisw2 = bool(pi.read(IMISW2_PIN))
        if  imisw0 and imisw1 and imisw2:
            break
    return bootst
    
if __name__ == '__main__':
    if main():
        # 正常終了。
        sys.exit()
    else:
        # 異常終了。全部停止させる。
        sys.exit(1)
