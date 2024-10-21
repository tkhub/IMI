import RPi.GPIO as GPIO
# from rpi_hardware_pwm import HardwarePWM
import pigpio
# TODO:pigpioに置き換えたい
class MOTORS:
    __EN_PIN : int    = 5
    __R_DIR_PIN :int  = 6
    __L_DIR_PIN : int = 16
    # __L_PLS_CH : int = 0
    # __R_PLS_CH : int = 1
    __L_PLS_PIN: int = 12
    __R_PLS_PIN: int = 13
    __PPS_MIN : int   = 4
    __PPS_MAX : int   = 4000
    __PIGPIOPWM_DUTYGAIN : int = 10000 
    __STOP_DUTY : int = 100
    __START_DUTY : int = 50
    __DEFAULT_FRQ : int = 1000
    __cnstcnt : int = 0
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__EN_PIN, GPIO.OUT)
        GPIO.setup(self.__L_DIR_PIN, GPIO.OUT)
        GPIO.setup(self.__R_DIR_PIN, GPIO.OUT)
        GPIO.output(self.__EN_PIN, False) # モータは止めておく
        self.__PIGPIO = pigpio.pi()
        # self.__L_PLS = HardwarePWM(pwm_channel=self.__L_PLS_CH, hz=100)
        # self.__R_PLS = HardwarePWM(pwm_channel=self.__R_PLS_CH, hz=100)
        self.__PIGPIO.hardware_PWM(self.__L_PLS_PIN, self.__DEFAULT_FRQ, int(self.__STOP_DUTY*self.__PIGPIOPWM_DUTYGAIN))
        self.__PIGPIO.hardware_PWM(self.__R_PLS_PIN, self.__DEFAULT_FRQ, int(self.__STOP_DUTY*self.__PIGPIOPWM_DUTYGAIN))
        self.__cnstcnt += 1
        # self.__L_PLS.start(100)
        # self.__R_PLS.start(100)

    def __del__(self):
            self.stop()
            GPIO.cleanup(self.__EN_PIN)
            GPIO.cleanup(self.__L_DIR_PIN)
            GPIO.cleanup(self.__R_DIR_PIN)
            self.__cnstcnt -= 1
    
    def close(self):
        self.stop()
        self.__del__()

    def start(self):
        GPIO.output(self.__EN_PIN, True)

    def stop(self):
        GPIO.output(self.__EN_PIN, False)

    def run(self, leftpps:int, rightpps:int) -> tuple[int, int]:
        leftppsrslt : int = 0
        rightppsrslt : int = 0
        if  abs(leftpps) < abs(self.__PPS_MIN) or \
            abs(leftpps) > abs(self.__PPS_MAX) :
            self.__PIGPIO.hardware_PWM(self.__L_PLS_PIN, self.__DEFAULT_FRQ, int(self.__STOP_DUTY*self.__PIGPIOPWM_DUTYGAIN))
            leftppsrslt = 0
        else:
            if leftpps < 0:
                GPIO.output(self.__L_DIR_PIN, True)
            else :
                GPIO.output(self.__L_DIR_PIN, False)
            # self.__L_PLS.change_frequency(abs(leftpps))
            self.__PIGPIO.hardware_PWM(self.__L_PLS_PIN, abs(leftpps), int(self.__START_DUTY*self.__PIGPIOPWM_DUTYGAIN))
            leftppsrslt = leftpps

        if  abs(rightpps) < abs(self.__PPS_MIN) or \
            abs(rightpps) > abs(self.__PPS_MAX) :
            self.__PIGPIO.hardware_PWM(self.__R_PLS_PIN, self.__DEFAULT_FRQ, int(self.__STOP_DUTY*self.__PIGPIOPWM_DUTYGAIN))
            rightpps = 0
        else:
            if rightpps < 0:
                GPIO.output(self.__R_DIR_PIN, False)
            else :
                GPIO.output(self.__R_DIR_PIN, True)
            self.__PIGPIO.hardware_PWM(self.__R_PLS_PIN, abs(rightpps), int(self.__START_DUTY*self.__PIGPIOPWM_DUTYGAIN))
            rightppsrslt = rightpps
        return (leftppsrslt, rightppsrslt)