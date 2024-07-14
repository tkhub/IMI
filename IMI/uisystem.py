from enum import Enum, auto


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import board
import busio
import adafruit_ssd1306
# from libs.devices.key import key as UiKeys
# from libs.devices.driver.uiled import uiled as UiLEDs


class UiSystem:

    # __KEYS:UiKeys
    __I2C:busio
    __DRAW:ImageDraw
    # __LEDS:UiLEDs
    __DSPADDR:hex = 0x3C
    __DSP:adafruit_ssd1306
    __FONT:ImageFont
    __cnstcnt:int = 0
    __testcnt:int
    def __init__(self) -> None:
        # self.__KEYS = UiKeys.Key()
        # self.__LEDS = UiLEDs.UILED()
        self.__I2C = busio.I2C(board.SCL, board.SDA)
        self.__DSP = adafruit_ssd1306.SSD1306_I2C(128, 64, self.__I2C, addr = self.__DSPADDR)
        img = Image.new("1", (self.__DSP.width, self.__DSP.height))
        self.__DRAW = ImageDraw.Draw(img)
        self.__DRAW.rectangle((0, 0, 128, 64), outline=255, fill=255)
        self.__FONT = ImageFont.load_default()
        text = "Hello World!"
        bbox = self.__FONT.getbbox(text)
        (font_width, font_height) = bbox[2] - bbox[0], bbox[3] - bbox[1]
        self.__DRAW.text(
            (128 // 2 - font_width // 2, 64 // 2 - font_height // 2),
            text,
            font=self.__FONT,
            fill=0,
        )
        self.__DSP.image(img)
        self.__DSP.show()
        self.__testcnt = 0
        self.__cnstcnt += 1

    def __del__(self):
        # self.__KEYS.close()
        # self.__LEDS.UILED.close
        self.__cnstcnt -= 1
    
    def close(self):
        self.__del__()

    def uiSystemExec(self):
        
        self.__testcnt += 1

    
