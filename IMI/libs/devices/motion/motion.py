import time
import sys
import math
sys.path.append('../')
import driver.motors 

class motion:
    __WIDTH : float = 87.0      # [mm] ホイールトレッド95mm - 8mm
    __WHEEL_D : float = 48.0    # [mm] ホイール直径
    __PPR : float = 400.0       # [パルス/周]
    __PI : float = math.pi      # [-]
    __MINV : float = 0.1        # [mm/s]
    __runTimeMIN : float = 0.01    # [sec]
    __x : float                 # [mm] 初期位置・方向での右
    __y : float                 # [mm] 初期位置・方向での左
    __deg : float               # [degrees]

    def __init__(self) -> None:
        self.md = driver.motors.MOTORS()
        self.__x = 0.0
        self.__y = 0.0
        self.__deg = 0.0
#    while True:
#        left = input("Left Speed(pps) = ")
#        right = input("Right Speed(pps) = ")
#        input("Press Any Key...")
#        motor.run(int(left), int(right))
        # motor.run(530, 528)
        # runTime.sleep(0.9*3)
        # motor.close()

    def __del__(self):
        if self.md != None:
            self.md.close()

    def close(self):
        if self.md != None:
            self.md.close()
    
    def start(self):
        self.md.start()

    def stop(self):
        self.md.stop()

    def pause(self):
        self.md.run(0,0)
    
    def run(self, speed_mmps:float = None, degrees:float = None, length :float = None, runTime:float = None, continueFlag:bool = True) -> (float, float,float):
        # omega = (Vr - Vl) / WIDTH
        # v = (Vr + Vl) / 2
        # deg = omega * runTime
        # runTime = 
        # 200 / (48 * PI) * 400 = 530.79
        
        errflg : bool = False
        # ユースケース1：超信地旋回 speed = 0, deg = x runTime = x
        # ユースケース2-1：スラローム speed = x, deg = x runTime = x
        # ユースケース2-2：直線 speed = x, deg = x length = x

        if (speed_mmps == None or (abs(speed_mmps) <= abs(self.__MINV))) \
            and degrees != None \
            and (runTime != None and (self.__runTimeMIN <= runTime)):
            # 超信地旋回モード：マスト=角度、時間情報
            # 180 * 3.14 / 0.5 / 180 / 87 / 2
            delta_v = (degrees/ runTime ) * self.__PI / 180 * self.__WIDTH / 2
            print(delta_v)
            Vr = -delta_v
            Vl = delta_v
        elif (speed_mmps != None and (abs(self.__MINV) < abs(speed_mmps))) \
            and degrees != None:
            # lenghtのみ指定の場合、runTimeを求める
            if length != None:
                runTime = length / speed_mmps
            if runTime != None and (self.__runTimeMIN <= runTime):
            # runTimeのみ指定の場合、runTimeが妥当ならdeltaVを計算
                delta_v = (degrees/ runTime ) * self.__PI / 180 * self.__WIDTH / 2
                print(delta_v)
            else :
                delta_v = 0

            Vr = speed_mmps - delta_v
            Vl = speed_mmps + delta_v

        else :
            Vr = 0
            Vl = 0

        vr_pps = (Vr / (self.__PI  * self.__WHEEL_D)) * self.__PPR
        vl_pps = (Vl / (self.__PI  * self.__WHEEL_D)) * self.__PPR
        self.md.run(int(vl_pps), int(vr_pps))
        if runTime != None:
            time.sleep(runTime)
        if continueFlag == False:
            self.md.run(int(0), int(0))
        self.__deg += degrees
        return (vl_pps, vr_pps, runTime)

    def position(self) -> (float, float, float):
        return (self.__x, self.__y, self.__deg)

    def collect(self, x:float == None, y:float == None, deg:float == None) -> (float, float, float):
        if x != None:
            self.__x == x
        if y != None:
            self.__y == y
        if deg != None:
            self.__deg == deg
        pass
    