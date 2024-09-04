from lzma import CHECK_CRC64
import spidev
from enum import Enum, IntEnum
import pigpio


class MCP3xxx:
#     #          Q4↖    ↗Q3         
#     #          CH0       CH3        
#     #          D12       D6         
#     #                               
#     #                               
#     #   Q5↑                   ↑Q2 
#     #  CH1                      CH2 
#     #  D13                      D5  
#     #  FL(17)                   FR(27)       
#     FL : int = 1
#     FR : int = 2
#     RR : int = 3
#     LL : int = 0
#     BAT : int = 4
    class SPIchannel(IntEnum):
        CH_0 = 0
        CH_1 = 1
        CH_2 = 2

    class resolution(Enum):
        BIT_12 = 12
        BIT_10 = 10
        
    class ChannelNum(Enum):
        CH_4 = 4
        CH_8 = 8
    __pi:pigpio.pi
    __cnstcnt : int = 0
    __RESOLUTION:resolution
    __CHNUM:ChannelNum
    #  b  b  b  b  b  b  R  T  n  n  n  n  W  A u2  u1 u0 p2  p1  p0  m m
    #                                         x x/0 x/0 x/0 x/0 x/0 x/0 0 0
    __SPIFLG:int = 0x0000
    
    def __init__(self, spichannel:SPIchannel = SPIchannel.CH_0, speed:int = 500000, bit_10_12:resolution= resolution.BIT_12, chnum:ChannelNum = ChannelNum.CH_4) -> None:
        self.__pi = pigpio.pi()
        self.__CHNUM = chnum
        self.__RESOLUTION = bit_10_12
        self.__spi = self.__pi.spi_open(spi_channel=int(spichannel), baud=speed, spi_flags = self.__SPIFLG)
        self.__cnstcnt += 1

    def __del__(self):
        if 0 < self.__cnstcnt:
            self.__pi.spi_close(self.__spi)
            self.__cnstcnt -= 1

    def close(self):
        self.__del__()
        
    def __genbit(self, readch : int) -> list[int]:
        bytesdat = 0x0000AA | 0x060000 | (int(readch) << 14)
        senddat :list[int] = [0, 0, 0]
        if self.__RESOLUTION == self.resolution.BIT_10:
            bytesdat = bytesdat >> 2
        senddat[0] = (bytesdat >> 16) & 0xFF
        senddat[1] = (bytesdat >> 8) & 0xFF
        senddat[2] = (bytesdat) & 0xFF
        return senddat

    def __convdat(self, dat: list[int]) -> int:
        if self.__RESOLUTION == self.resolution.BIT_12:
            adc = ((dat[1] & 0x0F) << 8) | dat[2]
        else :
            adc = ((dat[1] & 0x03) << 8) | dat[2]
        return adc

    def read(self, readch:int) -> int:
        # count:int
        # rawList:any
        val:int = 0
        (_, rawList) = self.__pi.spi_xfer(self.__spi, self.__genbit(readch))
        val = self.__convdat(rawList)
        return val
