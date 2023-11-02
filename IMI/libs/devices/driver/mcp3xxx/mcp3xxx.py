import spidev

class MCP3XXX:
    #          Q4↖    ↗Q3         
    #          CH0       CH3        
    #          D12       D6         
    #                               
    #                               
    #   Q5↑                   ↑Q2 
    #  CH1                      CH2 
    #  D13                      D5  
    #  FL(17)                   FR(27)       
    FL : int = 1
    FR : int = 2
    RR : int = 3
    LL : int = 0
    BAT : int = 4
    __cnstcnt : int = 0
    def __init__(self, spi_channel = 0, speed = 1000000, bit = 12, chnum = 4) -> None:
        self.__spibus = 0
        self.__spi_channel = spi_channel
        self.__max_speed_hz = speed 
        self.__spi = spidev.SpiDev()
        self.__cnstcnt += 1
        if bit == 12:
            self.__bit = 12
        else:
            self.__bit = 10
        if chnum == 8:
            self.__chnum = 8
        else:
            self.__chnum = 4


    def __del__(self):
        if 0 < self.__cnstcnt:
            self.__spi = None
            self.__cnstcnt -= 1

    def close(self):
        self.__del__(self)

    def __genbit(self, readch : int) -> list[int]:
        bytesdat = 0x0000AA | 0x060000 | (readch << 14)
        senddat :int = [0] * 3
        if self.__bit == 10:
            bytesdat = bytesdat >> 2
        senddat[0] = (bytesdat >> 16) & 0xFF
        senddat[1] = (bytesdat >> 8) & 0xFF
        senddat[2] = (bytesdat) & 0xFF
        return senddat

    def __convdat(self, dat: list[int]) -> int:
        if self.__bit == 12:
            adc = ((dat[1] & 0x0F) << 8) | dat[2]
        else :
            adc = ((dat[1] & 0x03) << 8) | dat[2]
        return adc

    def read(self, readch = "all") -> int:
        self.__spi.open(self.__spibus, self.__spi_channel)
        self.__spi.max_speed_hz = self.__max_speed_hz
        
        if readch == "all":
            adc = [0] * self.__chnum
            for i in range(self.__chnum):
                val = self.__spi.xfer2(self.__genbit(i))
                adc[i] = self.__convdat(val)
        else :
            adc : int = 0
            if type(self.__chnum) == int:
                if readch < self.__chnum:
                    val = self.__spi.xfer2(self.__genbit(readch))
                    adc = self.__convdat(val)
                else:
                    adc = 0
        self.__spi.close()
        return adc

# def test(chnum) -> int:
#     spi = spidev.SpiDev()
#     spi.open(0,0)
#     spi.max_speed_hz = 500000
#     read_ch0 = [0x06 | 0b00000001, 0x00 | 0b00000000, 0x00]
#     adc = spi.xfer2(read_ch0)

#     data = ((adc[1] & 0x0F) << 8) | adc[2]
#     print(adc)
#     print(data)
#     spi.close()

