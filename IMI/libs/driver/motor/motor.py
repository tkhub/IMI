import RPi.GPIO as GPIO

class MOTOR:
    __MOTOR_EN_PIN : int    = 5
    __MOTOR_R_DIR_PIN :int  = 6
    __MOTOR_R_PLS_PIN : int = 13
    __MOTOR_L_DIR_PIN : int = 16
    __MOTOR_L_PLS_PIN : int = 12
    __MOTOR_PPS_MIN : int   = 4
    __MOTOR_PPS_MAX : int   = 4000

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__MOTOR_EN_PIN, GPIO.OUT)
        GPIO.setup(self.__MOTOR_L_DIR_PIN, GPIO.OUT)
        GPIO.setup(self.__MOTOR_R_DIR_PIN, GPIO.OUT)
        GPIO.setup(self.__MOTOR_L_PLS_PIN, GPIO.OUT)
        GPIO.setup(self.__MOTOR_R_PLS_PIN, GPIO.OUT)
        GPIO.output(self.__MOTOR_EN_PIN, False) # モータは止めておく
        self.__MOTOR_L_PLS = GPIO.PWM(self.__MOTOR_L_PLS_PIN, 10)
        self.__MOTOR_R_PLS = GPIO.PWM(self.__MOTOR_R_PLS_PIN, 10)
        self.__MOTOR_L_STATE:bool = False
        self.__MOTOR_R_STATE:bool = False
        self.__MOTOR_L_PLS.start(100)
        self.__MOTOR_R_PLS.start(100)

    def __del__(self):
        GPIO.cleanup(self.__MOTOR_EN_PIN)
        GPIO.cleanup(self.__MOTOR_L_DIR_PIN)
        GPIO.cleanup(self.__MOTOR_R_DIR_PIN)
        GPIO.cleanup(self.__MOTOR_L_PLS_PIN)
        GPIO.cleanup(self.__MOTOR_R_PLS_PIN)
    
    def close(self):
        self.__del__()
    
    def start(self):
        GPIO.output(self.__MOTOR_EN_PIN, True)

    def stop(self):
        GPIO.output(self.__MOTOR_EN_PIN, False)

    def run(self, leftpps:int, rightpps:int) -> (int, int):
        leftppsrslt : int = 0
        rightppsrslt : int = 0
        if  abs(leftpps) < abs(self.__MOTOR_PPS_MIN) or \
            abs(leftpps) > abs(self.__MOTOR_PPS_MAX) :
            if self.__MOTOR_L_STATE == True:
                self.__MOTOR_L_STATE = False
                self.__MOTOR_L_PLS.ChangeDutyCycle(100)
            leftppsrslt = 0
        else:
            if self.__MOTOR_L_STATE == False:
                self.__MOTOR_L_STATE = True
                self.__MOTOR_L_PLS.ChangeDutyCycle(50)
            if leftpps < 0:
                GPIO.output(self.__MOTOR_L_DIR_PIN, True)
            else :
                GPIO.output(self.__MOTOR_L_DIR_PIN, False)
            self.__MOTOR_L_PLS.ChangeFrequency(abs(leftpps))
            leftppsrslt = leftpps
        if  abs(rightpps) < abs(self.__MOTOR_PPS_MIN) or \
            abs(rightpps) > abs(self.__MOTOR_PPS_MAX) :
            if self.__MOTOR_R_STATE== True:
                self.__MOTOR_R_STATE = False
                self.__MOTOR_R_PLS.ChangeDutyCycle(100)
            rightpps = 0
        else:
            if self.__MOTOR_R_STATE == False:
                self.__MOTOR_R_STATE = True
                self.__MOTOR_R_PLS.ChangeDutyCycle(50)
            if rightpps < 0:
                GPIO.output(self.__MOTOR_R_DIR_PIN, False)
            else :
                GPIO.output(self.__MOTOR_R_DIR_PIN, True)
            self.__MOTOR_R_PLS.ChangeFrequency(abs(rightpps))
            rightppsrslt = rightpps
        return (leftppsrslt, rightppsrslt)