# TODO:付き当てモーションを加える
# TODO:直進、カーブ、Uターンをチェックする
import time
import os
import sys
import math
from tkinter import NO
from token import OP
from typing import Tuple, Optional
from typing_extensions import runtime
# sys.path.append('../')
# import driver.motors 
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from driver.motors import motors

class runmotion:
    class __PARAM:
        class SPIN:
            GAIN:float = 0.95
            OFFSET:float = 0
        class STRAIGHT:
            GAIN:float = 1.05
            OFFSET:float = 0
        class TURN:
            TURN_GAIN:float = 0.95
            TURN_OFFSET:float = 0
            LENGTH_GAIN:float = 1.05
            LENGTH_OFFSET:float = 0
    class __LIM:
        class SPEED:
            MIN:float = 0.1       # [mm/s]
            MAX:float = 2000.0    # [mm/s]
        class DEGREES:
            MIN:float = 0.1   # [deg]
            MAX:float = 359.999 # [deg]
        class RUNTIME:
            MIN:float = 0.01      # [sec]
        class LENGTH:
            MIN:float = 0.4       # [mm]
        class RADIUS:
            MIN:float = 0.1       # [mm]
            MAX:float = 1000.0    # [mm]
        class DEGV:
            MIN:float = 0.01      # [deg/s]
            MAX:float = 10        # [deg/s]
    class __SPECS:
        WIDTH:float   = 87.0  # [mm] ホイールトレッド (95mm - 8mm)
        WHEEL_D:float = 48.0  # [mm] ホイール直径
        PPR:int       = 400   # [ppr] ホイール1回転あたりのパルス

    __PI : float = math.pi      # [-]
    __x : float                 # [mm] 初期位置・方向での右
    __y : float                 # [mm] 初期位置・方向での左
    __deg : float               # [degrees]
    __cnstcnt : int = 0

    def __init__(self) -> None:
        #self.md = driver.motors.MOTORS()
        self.md = motors.MOTORS()
        self.__x = 0.0
        self.__y = 0.0
        self.__deg = 0.0
        self.__cnstcnt += 0

    def __del__(self):
        if 0 < self.__cnstcnt:
            self.pause()
            self.stop()
            self.md.close()

    def close(self):
        self.__del__()

    def start(self):
        self.md.start()

    def stop(self):
        self.md.stop()

    def pause(self):
        self.md.run(0,0)
    
    def run(    self, speed_mmps:Optional[float] = None, 
                degrees:Optional[float] = None, 
                length:Optional[float] = None, 
                degv:Optional[float] = None,
                radius:Optional[float] = None,
                runperiod:Optional[float] = None, 
                continueFlag:bool = True) -> Tuple[float, float, float, float, float,float]:
        """_summary_

        Args:
            speed_mmps (Optional[float], optional): 走行速度[mm/s]. Defaults to None.
            degrees (Optional[float], optional): 回転角度[°]右回転を正. Defaults to None.
            length (Optional[float], optional): _description_. Defaults to None.
            degv (Optional[float], optional): _description_. Defaults to None.
            radius (Optional[float], optional): _description_. Defaults to None.
            runperiod (Optional[float], optional): _description_. Defaults to None.
            continueFlag (bool, optional): _description_. Defaults to True.

        Returns:
            Tuple[float, float, float, float, float,float]: _description_
        """        
        rotatept:Optional[float] = None
        calRadius:Optional[float] = None
        calPeriod:Optional[float] = None
        delta_v:float = 0.0
        vr_pps:float = 0.0
        vl_pps:float = 0.0

        Vr:float = 0.0
        Vl:float = 0.0

        # 各種入力値のエラー対処。
        # speed 正負と0とNoneのみにする
        speedf:float = 0.0
        if speed_mmps is None:
            speedf = 0.0
        elif abs(speed_mmps) < abs(self.__LIM.SPEED.MIN):
            speedf = 0.0
            speed_mmps = None
        elif speed_mmps > self.__LIM.SPEED.MAX:
            speedf = self.__LIM.SPEED.MAX
            speed_mmps = self.__LIM.SPEED.MAX
        elif speed_mmps < -(self.__LIM.SPEED.MAX):
            speedf = -(self.__LIM.SPEED.MAX)
            speed_mmps = -(self.__LIM.SPEED.MAX)
        else:
            speedf = speed_mmps

        # degrees -360～+360とNoneのみにする
        degreesf:float = 0.0
        if degrees is None:
            degreesf = 0.0
        elif abs(degrees) < abs(self.__LIM.DEGREES.MIN):
            degreesf = 0.0
            degrees = None
        else:
            if degrees >= self.__LIM.DEGREES.MAX:
                degrees = self.__LIM.DEGREES.MAX
            if degrees <= -(self.__LIM.DEGREES.MAX):
                degrees = -(self.__LIM.DEGREES.MAX)
            degreesf = degrees 

        # runtime 正の値かNone
        runtimef:float = 0.0
        if runperiod is None:
            runtimef = 0.0
        elif runperiod < self.__LIM.RUNTIME.MIN:
            runperiod = None
            runtimef = 0.0
        else:
            runtimef = runperiod

        # radius ある程度までの正の値かNone
        radiusf:float = 0.0
        if radius is None:
            radiusf = 0.0
        elif radius < self.__LIM.RADIUS.MIN:
            radius = None
            radiusf = 0.0
        elif radius > self.__LIM.RADIUS.MAX:
            radius = self.__LIM.RADIUS.MAX
            radiusf = self.__LIM.RADIUS.MAX
        else:
            radiusf = radius
        
        # lenght 正の値かNone
        lengthf:float = 0.0
        if length is None:
            lengthf = 0.0
        elif length < self.__LIM.LENGTH.MIN:
            lengthf = 0.0
            length = None
        else:
            lengthf = length

        # degv 正の値かNone
        degvf:float = 0.0
        if degv is None:
            degvf = 0.0
        elif degv < self.__LIM.DEGV.MIN:
            degvf = 0.0
            degv = None
        elif degv > self.__LIM.DEGV.MAX:
            degvf = self.__LIM.DEGV.MAX
            degv = self.__LIM.DEGV.MAX
        else:
            degvf = degv

        # 超信地旋回
        # speedが指定ないなら超信地旋回
        # speed = 0、degはマスト
        # runtimeかdegvが指示されたら回る
        # length, radiusは無視
        # 
        if      (speed_mmps == None) \
            and (degrees != None) \
            and (runperiod != None or degv != None):

            adjd_degrees = degrees * self.__PARAM.SPIN.GAIN + self.__PARAM.SPIN.OFFSET

            # 
            if runperiod is None and degv is not None:
                # 角度[deg]と角速度[deg/s]から回転時間を求める
                rotatept = abs(degrees / degv)
            elif runperiod is not None:
                # 時間が指定されている場合はそのまま
                rotatept = runperiod
            else:
                pass
            
            if rotatept is not None:
                delta_v = (adjd_degrees/ rotatept) * self.__PI / 180 * self.__SPECS.WIDTH / 2
                Vr = -delta_v
                Vl = delta_v
                calRadius = None
                calPeriod = rotatept
            # ここには到達しないはず
            else:
                Vr = 0
                Vl = 0
                calRadius = None

                

        # 直進
        elif        speed_mmps is not None and degrees is None \
                and (length is not None or runperiod is not None):
            if length is not None:
                rotatept = abs((length * self.__PARAM.STRAIGHT.GAIN + self.__PARAM.STRAIGHT.OFFSET)/ speed_mmps)
                calPeriod = abs(length / speed_mmps)
            Vr = speed_mmps
            Vl = speed_mmps
            calRadius = None
        # 旋回 速度と角度はマスト。角速度を求めて左右輪の差を求めるために、角速度か、半径か
        elif        speed_mmps is not None and degrees is not None \
                and (length is not None or runperiod is not None or radius is not None):
            adjd_degrees = degrees * self.__PARAM.TURN.TURN_GAIN+ self.__PARAM.TURN.TURN_OFFSET
            print("Turn")
            # lengthのみ分かる→速度からrunperiodを求め、degとrunperiodからdegvを求める。degvかららΔVを求める
            if length is not None:
                # 距離から直接走行時間を求める
                rotatept = abs((length * self.__PARAM.TURN.LENGTH_GAIN + self.__PARAM.TURN.LENGTH_OFFSET )/ speed_mmps)
                # 時間からdegvを求める
                delta_v = (adjd_degrees/ rotatept) * self.__PI / 180 * self.__SPECS.WIDTH / 2
                # 計算上の半径
                calRadius = speed_mmps / ( (degrees / rotatept) * self.__PI / 180.0)
                # 計算上の時間
                calPeriod = abs(length / speed_mmps)
                print(f"length = {length}")
            
            # degvのみ分かる→degとdegvからrunperiodを求める。degvからΔVを求める。
            elif degv is not None:
                # 目標角度と角速度から走行時間を求める
                rotatept = abs(degrees / degv)
                # degvそのままつかえる
                delta_v = degv * self.__PI / 180 * self.__SPECS.WIDTH / 2
                # 計算上の半径
                calRadius = speed_mmps / ( degv * self.__PI / 180.0)
                # 計算上の時間
                calPeriod = abs(degrees / degv)
                print(f"degv = {degv}")

            # radiusのみ分かる→radiusから直接ΔVを求める。radiusとdegとspeedからrunperiodを求める
            elif radius is not None:
                # 目標角度と半径と速度から走行時間を求める
                rotatept = abs(((degrees / 360.0) * 2.0 * self.__PI * radius) / speed_mmps)
                # runperiodのみ分かる→runperiodとdegからdegvを求める。degvからΔVを求める。
                delta_v = (adjd_degrees/ rotatept) * self.__PI / 180 * self.__SPECS.WIDTH / 2
                # 計算上の半径
                calRadius = radius
                # 計算上の時間
                calPeriod = abs(((degrees / 360.0) * 2.0 * self.__PI * radius) / speed_mmps)
                print(f"radius = {radius}")
            Vr = speed_mmps - delta_v
            Vl = speed_mmps + delta_v

        vr_pps = (Vr / (self.__PI  * self.__SPECS.WHEEL_D)) * float(self.__SPECS.PPR)
        vl_pps = (Vl / (self.__PI  * self.__SPECS.WHEEL_D)) * float(self.__SPECS.PPR)
        self.__updatepos(speed=speed_mmps,degrees=degrees,radius=calRadius,period=calPeriod)
        if rotatept is not None:
            self.md.run(int(vl_pps), int(vr_pps))
            time.sleep(rotatept)
            if continueFlag == False:
                self.md.run(int(0), int(0))
            return (vl_pps, vr_pps, rotatept, self.__x, self.__y, self.__deg)
        else:
            self.md.run(0, 0)
            return (0, 0, 0, self.__x, self.__y, self.__deg)

        

    def __updatepos(self, speed:Optional[float], degrees:Optional[float], radius:Optional[float], period:Optional[float]) -> Tuple[float, float, float]:
        # スピンモード
        if speed is None:
            if degrees is not None:
                self.__deg += degrees
                if 360.00 < self.__deg:
                    self.__deg = self.__deg - 360.00
                if self.__deg < 0.0:
                    self.__deg = 360.0 + self.__deg
            else:
                pass
        else:
            # 直進の場合、速度と走行時間は必須
            if degrees is None and period is not None:
                # 今向いている角度に一定速度である時間進んだ場合の座標を計算
                self.__x += speed * period * math.cos(math.radians(self.__deg))
                self.__y += speed * period * math.sin(math.radians(self.__deg))
            elif degrees is not None and radius:
                chorod:float = 2 * radius * math.sin(math.radians(degrees/2))
                print(f"chorod = {chorod}")
                print(f"deg = {degrees}")
                self.__x += chorod * math.cos(math.radians(degrees / 2 + self.__deg))
                self.__y += chorod * math.sin(math.radians(degrees / 2 + self.__deg))
                self.__deg += degrees
                if 360.00 < self.__deg:
                    self.__deg = self.__deg - 360.00
                if self.__deg < 0.0:
                    self.__deg = 360.0 + self.__deg
            else:
                pass
        return (self.__x, self.__y, self.__deg)

    def position(self) -> tuple[float, float, float]:
        return (self.__x, self.__y, self.__deg)

    def collect(self, x:Optional[float] = None, y: Optional[float] = None, deg:Optional[float] = None) -> tuple[float, float, float]:
        if x != None:
            self.__x = x
        if y != None:
            self.__y = y
        if deg != None:
            self.__deg = deg
        return (self.__x, self.__y, self.__deg)

    # class grid:
    #     __X_GAIN = -0.3
    #     __STHF_LEN = 90.0
    #    .TURN_HFST_LEN = 90.0
    #     __R_TRUN_ANGL = +90.0
    #     __L_TRUN_ANGL = -90.0
    #     __U_TRUN_ANGL = +180.0

    # def __init__(self) -> None:
    #     self.MVMOTION = motion.motion()
    #     self.WLSNS = wallsensors.wallsensors()
    #     self.MAZE_SIZE : float = 180.0
    #     self.__cnstcnt  += 1
    #     self.MVMOTION.start()
    
    # def __del__(self):
    #     self.close()
    
    # def close(self):
    #     if 0 < self.__cnstcnt:
    #         self.MVMOTION.stop()
    #         self.MVMOTION.close()
    #         self.WLSNS.close()

    # def straight(self, speed:float, grids:int, contFlag:bool = True):
    #     adjust_deg:float = 0
    #     wsns = (False, False, False, 0.0, 0.0, 0.0)
    #     for i in range(grids * 2 -1):
    #         wsns = self.WLSNS.read()
    #         adjust_deg = wsns[3] * self.__X_GAIN
    #         self.MVMOTION.run(speed_mmps=speed, degrees = adjust_deg, length=self.__STHF_LEN, continueFlag=True)
    #     self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.__STHF_LEN, continueFlag=contFlag)
    #     if contFlag == False:
    #         sleep(0.05)
    #     pos = self.MVMOTION.position()
    #     return (wsns[0], wsns[1],wsns[2],wsns[3],wsns[4],wsns[5], pos[0], pos[1], pos[2])

    # def straight_hf(self, speed:float,contFlag:bool = True):
    #     wsns = self.WLSNS.read()
    #     self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.__STHF_LEN, continueFlag=contFlag)
    #     pos = self.MVMOTION.position()
    #     return (wsns[0], wsns[1],wsns[2],wsns[3],wsns[4],wsns[5], pos[0], pos[1], pos[2])

    # def left(self, speed:float):
    #     self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.TURN_HFST_LEN, continueFlag=False)
    #     sleep(0.1)
    #     self.MVMOTION.run(speed_mmps=speed, degrees = self.__L_TRUN_ANGL, runperiod=0.5, continueFlag=False)
    #     sleep(0.1)
    #     self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.MAZE_SIZE/2, continueFlag=False)
    #     wsns = self.WLSNS.read()
    #     pos = self.MVMOTION.position()
    #     return (wsns[0], wsns[1],wsns[2],wsns[3],wsns[4],wsns[5], pos[0], pos[1], pos[2])

    # def right(self, speed:float):
    #     self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.MAZE_SIZE/2, continueFlag=False)
    #     sleep(0.1)
    #     self.MVMOTION.run(speed_mmps=speed, degrees = self.__R_TRUN_ANGL, runperiod=0.5, continueFlag=False)
    #     sleep(0.1)
    #     self.MVMOTION.run(speed_mmps=speed, degrees = 0, length=self.MAZE_SIZE/2, continueFlag=False)
    #     wsns = self.WLSNS.read()
    #     pos = self.MVMOTION.position()
    #     return (wsns[0], wsns[1],wsns[2],wsns[3],wsns[4],wsns[5], pos[0], pos[1], pos[2])

    # def u_turn(self, speed:float):
    #     self.MVMOTION.run(speed_mmps=speed, degrees = self.__U_TRUN_ANGL, runperiod=1.5, continueFlag=False)
    #     self.MVMOTION.run(speed_mmps=-speed, degrees = 0, length=self.MAZE_SIZE/2, continueFlag=False)
    #     wsns = self.WLSNS.read()
    #     pos = self.MVMOTION.position()
    #     return (wsns[0], wsns[1],wsns[2],wsns[3],wsns[4],wsns[5], pos[0], pos[1], pos[2])

    # def l_turn(self, mtime:float = 1.0):
    #     self.MVMOTION.run(speed_mmps=0, degrees = self.__L_TRUN_ANGL, runperiod=mtime, continueFlag=False)
    #     sleep(0.5)

    # def r_turn(self, mtime:float = 1.0):
    #     self.MVMOTION.run(speed_mmps=0, degrees = self.__R_TRUN_ANGL, runperiod=mtime, continueFlag=False)
    #     sleep(0.5)

