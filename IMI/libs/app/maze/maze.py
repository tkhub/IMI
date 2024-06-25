from typing import Optional
from math import sin, cos, radians, floor
from enum import Enum
class Maze:
    class Grid:
        position_x:int
        position_y:int
        n_wall:Optional[bool]
        w_wall:Optional[bool]
        e_wall:Optional[bool]
        s_wall:Optional[bool]
        g_step:Optional[int]
        class WayFinding(Enum):
            NOWAY       = 0
            NORTH = 1
            SOUTH = 2
            EAST = 3
            WEST = 4
        goal_way:Optional[WayFinding]
        def __init__(self):
            self.n_wall = None
            self.s_wall = None
            self.e_wall = None
            self.w_wall = None
            self.g_step = None
            self.goal_way = self.WayFinding.NOWAY

    class Grids:
        def __init__(self, grid = None):
            self.child1 = None
            self.child2 = None
    INDEX_X:int = 0
    INDEX_Y:int = 1
    INDEX_NORTH:int = 0
    INDEX_SOUTH:int = 1
    INDEX_EAST:int = 2
    INDEX_WEST:int = 3
    INDEX_Y:int = 1
    __GOAL_SIZE_X :int = 2
    __GOAL_SIZE_Y :int = 2
    __MAZE_GRID_SIZE:int = 180
    __GOAL_POSITION_X:int
    __GOAL_POSITION_Y:int
    __MAZE_MAX_X :int
    __MAZE_MAX_Y :int
    __MAZE_MIN_X :int
    __MAZE_MIN_Y :int
    __MAZE_OCEAN : int
    
    #             0  MIN_X ........ MAX_X..len(list[0])
    #          0.....................................
    #           .....................................
    #      MIN_Y.....................................
    #           .....................................
    #           .....................................
    #           .....................................
    #      MAX_X.....................................
    #           .....................................
    #  len(list).....................................

    def __init__(self, maze_size:tuple[int,int], goal:tuple[int, int]) -> None:
        self.__MAZE_MIN_X = 1
        self.__MAZE_MIN_Y = 1
        self.__MAZE_MAX_X = maze_size[self.INDEX_X] + self.__MAZE_MIN_X -1
        self.__MAZE_MAX_Y = maze_size[self.INDEX_Y] + self.__MAZE_MIN_Y -1
        self.__MAZE_OCEAN = maze_size[self.INDEX_X] * maze_size[self.INDEX_Y] + 2
        self.__GOAL_POSITION_X = goal[self.INDEX_X] + self.__MAZE_MIN_X
        self.__GOAL_POSITION_Y = goal[self.INDEX_Y] + self.__MAZE_MIN_Y
        self.__MAZE_GRIDS = [[self.Grid() for y in range(self.__MAZE_MAX_Y + 2)] for x in range(self.__MAZE_MAX_X + 2)]
        for x, grids_y in enumerate(self.__MAZE_GRIDS):
            for y, grid in enumerate(grids_y):
                # 周囲を壁で埋める
                # 周囲を高いステップ数で埋める
                if x == 0:
                    if y != 0 or y != self.__MAZE_MAX_Y + 1:
                        grid.w_wall = True
                    grid.g_step = self.__MAZE_OCEAN
                if x == self.__MAZE_MIN_X:
                    grid.e_wall = True
                if x == (len(self.__MAZE_GRIDS) - 1):
                    if y != 0 or y != self.__MAZE_MAX_Y + 1:
                        grid.e_wall = True
                    grid.g_step = self.__MAZE_OCEAN
                if x == self.__MAZE_MAX_X:
                    grid.w_wall = True

                if y == 0:
                    if x != 0 or x != self.__MAZE_MAX_X + 1:
                        grid.n_wall = True
                    grid.g_step = self.__MAZE_OCEAN
                if y == self.__MAZE_MIN_Y:
                    grid.s_wall = True
                if y == len(grids_y) - 1:
                    grid.s_wall = True
                    grid.g_step = self.__MAZE_OCEAN
                if y == self.__MAZE_MAX_Y:
                    grid.n_wall = True
                # ゴールのステップ数を入れる
                if self.__isGoal((x,y)):
                    grid.g_step = 0
                grid.goal_way = self.Grid.WayFinding.NOWAY
        # スタート地点の壁
        self.__MAZE_GRIDS[self.__MAZE_MIN_X][self.__MAZE_MIN_Y].n_wall = False
        self.__MAZE_GRIDS[self.__MAZE_MIN_X][self.__MAZE_MIN_Y + 1].s_wall = False
        self.__MAZE_GRIDS[self.__MAZE_MIN_X][self.__MAZE_MIN_Y].w_wall = True
        self.__MAZE_GRIDS[self.__MAZE_MIN_X + 1][self.__MAZE_MIN_Y].e_wall = True
        self.__MAZE_GRIDS[self.__MAZE_MIN_X][self.__MAZE_MIN_Y].goal_way = self.Grid.WayFinding.NORTH
    
    def __isGoal(self, position:(int,int)) -> bool:
        if      (   self.__GOAL_POSITION_X == position[self.INDEX_X] - self.__MAZE_MIN_X \
            or      self.__GOAL_POSITION_X == (position[self.INDEX_X] - self.__MAZE_MIN_X + self.__GOAL_SIZE_X - 1)) \
            and (   self.__GOAL_POSITION_Y == position[self.INDEX_Y] - self.__MAZE_MIN_Y \
            or      self.__GOAL_POSITION_Y == (position[self.INDEX_Y] - self.__MAZE_MIN_Y + self.__GOAL_SIZE_Y - 1)):
            return True
        else:
            return False
    def isReached(  self, position_xy=tuple[int,int]) -> bool:
        pindex_xy = (position_xy[self.INDEX_X] + self.__MAZE_MIN_X, position_xy[self.INDEX_Y] + self.__MAZE_MIN_Y)
        if (        self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].n_wall != None  \
                and self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].s_wall != None  \
                and self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].e_wall != None  \
                and self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].w_wall != None ):
            return True
        else :
            return False

    def updateWall(  self, position_xy=tuple[int,int], walls_nsew:tuple[Optional[bool], Optional[bool],Optional[bool],Optional[bool]] = (None, None, None, None)):
        """
            @brief 壁情報の更新
            :param position_xy: 壁情報を更新する座標(マス目、絶対値、スタートが0,0)
            :param walls_nsew: センサで取得した壁の有無。N,S、E、Wの並び。壁があればTrue、壁がなければFalse、解らなければNone
        """
        pindex_xy = (position_xy[self.INDEX_X] + self.__MAZE_MIN_X, position_xy[self.INDEX_Y] + self.__MAZE_MIN_Y)
        if      pindex_xy[self.INDEX_X] < self.__MAZE_MIN_X or self.__MAZE_MAX_X < pindex_xy[self.INDEX_X] \
            or  pindex_xy[self.INDEX_Y] < self.__MAZE_MIN_Y or self.__MAZE_MAX_Y < pindex_xy[self.INDEX_Y] :
            print("EXIT")
        else:
            # 北壁更新あり かつ 迷路の北端でない
            if walls_nsew[self.INDEX_NORTH]!= None and pindex_xy[self.INDEX_Y] != self.__MAZE_MAX_Y:
                # 北壁あり
                if walls_nsew[self.INDEX_NORTH] == True:
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].n_wall = True
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y] + 1].s_wall = True
                # 北壁なし
                else:
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].n_wall = False
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y] + 1].s_wall = False

            # 南壁更新あり かつ 迷路の南端でない
            if walls_nsew[self.INDEX_SOUTH]!= None and pindex_xy[self.INDEX_Y] != self.__MAZE_MIN_Y:
                # 南壁あり
                if walls_nsew[self.INDEX_SOUTH] == True:
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].s_wall = True
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y] - 1].n_wall = True
                # 南壁なし
                else:
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].s_wall = False
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y] - 1].n_wall = False

            # 東壁更新あり かつ 迷路の東端でない
            if walls_nsew[self.INDEX_WEST]!= None and pindex_xy[self.INDEX_X] != self.__MAZE_MAX_X:
                # 東壁あり
                if walls_nsew[self.INDEX_WEST] == True:
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].w_wall = True
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X] + 1][pindex_xy[self.INDEX_Y]].e_wall = True
                # 東壁なし
                else:
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].w_wall = False
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X] + 1][pindex_xy[self.INDEX_Y]].e_wall = False

            # 西壁更新あり かつ 迷路の西端でない
            if walls_nsew[self.INDEX_EAST]!= None and pindex_xy[self.INDEX_X] != self.__MAZE_MIN_X:
                # 西壁あり
                if walls_nsew[self.INDEX_EAST] == True:
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].e_wall = True
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X] - 1][pindex_xy[self.INDEX_Y]].w_wall = True
                # 西壁なし
                else:
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X]][pindex_xy[self.INDEX_Y]].e_wall = False
                    self.__MAZE_GRIDS[pindex_xy[self.INDEX_X] - 1][pindex_xy[self.INDEX_Y]].w_wall = False


    def show(self, position:tuple[Optional[int], Optional[int]] = (None, None)) :
        mazestrH:str
        mazestrM:str
        mazestrL:str
        num:int
        yi:int
        for y in range(len(self.__MAZE_GRIDS[0])):
            yi = len(self.__MAZE_GRIDS[0]) - y - 1
            if y == 0:
                mazestrH ="  W  N "
            else:
                mazestrH ="       "

            if 0 != y and y != (len(self.__MAZE_GRIDS[0]) - 1):
                mazestrM = "  Y" + str(yi - 1).rjust(3) + " "
            else:
                mazestrM = "       "

            if y == (len(self.__MAZE_GRIDS[0]) - 1):
                mazestrL ="  W  S "
            else:
                mazestrL ="       "

            for x in range(len(self.__MAZE_GRIDS)):
                if self.__MAZE_GRIDS[x][yi].n_wall == False :
                    mazestrH += "+       +"
                elif self.__MAZE_GRIDS[x][yi].n_wall == True:
                    mazestrH += "+-------+"
                else:
                    mazestrH += "+  - -  +"

                if self.__MAZE_GRIDS[x][yi].e_wall == True:
                    mazestrM += "|"
                elif self.__MAZE_GRIDS[x][yi].e_wall == False:
                    mazestrM += " "
                else :
                    mazestrM += ":"

                # フラグ表示
                if self.__isGoal((x,yi)) == True:
                    mazestrM += " G"
                elif x == self.__MAZE_MIN_X and yi == self.__MAZE_MIN_Y:
                    mazestrM += " S"
                elif self.__MAZE_GRIDS[x][yi].goal_way != None:
                    if self.__MAZE_GRIDS[x][yi].goal_way == self.__MAZE_GRIDS[x][yi].WayFinding.EAST:
                        mazestrM += " <"
                    elif self.__MAZE_GRIDS[x][yi].goal_way == self.__MAZE_GRIDS[x][yi].WayFinding.WEST:
                        mazestrM += " >"
                    elif self.__MAZE_GRIDS[x][yi].goal_way == self.__MAZE_GRIDS[x][yi].WayFinding.NORTH:
                        mazestrM += " ^"
                    elif self.__MAZE_GRIDS[x][yi].goal_way == self.__MAZE_GRIDS[x][yi].WayFinding.SOUTH:
                        mazestrM += " V"
                    else:
                        mazestrM += " *"
                else:
                    mazestrM += "  "

                if self.__MAZE_GRIDS[x][yi].g_step == self.__MAZE_OCEAN:
                    mazestrM += "     "
                elif self.__MAZE_GRIDS[x][yi].g_step != None:
                    mazestrM += str(self.__MAZE_GRIDS[x][yi].g_step).rjust(4) + " "
                else:
                    mazestrM += ".... "
                
                if self.__MAZE_GRIDS[x][yi].w_wall == True:
                    mazestrM += "|"
                elif self.__MAZE_GRIDS[x][yi].w_wall == False:
                    mazestrM += " "
                else:
                    mazestrM += ":"

                if self.__MAZE_GRIDS[x][yi].s_wall == True:
                    mazestrL += "+-------+"
                elif self.__MAZE_GRIDS[x][yi].s_wall == False:
                    mazestrL += "+       +"
                else:
                    mazestrL += "+  - -  +"
            print(mazestrH)
            print(mazestrM)
            print(mazestrL)
        mazestrH ="               "
        for x in range(self.__MAZE_MIN_X,self.__MAZE_MAX_X + 1):
            mazestrH += "  X" + str(x-1).ljust(3) + "   "
        mazestrH += "      S  E"
        print(mazestrH)

    def refreshStep(self):
        for x in range(self.__MAZE_MIN_X, self.__MAZE_MAX_X + 1):
            for y in range(self.__MAZE_MIN_Y, self.__MAZE_MAX_Y + 1):
            #      if self.__isGoal() != True:
                if self.__isGoal((x,y)) == True:
                    self.__MAZE_GRIDS[x][y].g_step = 0
                else:
                    self.__MAZE_GRIDS[x][y].g_step = None

    def calcStep(self):
        cnt:int = 0
        loopContinue:bool = True 
        while loopContinue:
            for x in range(self.__MAZE_MIN_X, self.__MAZE_MAX_X + 1):
                for y in range(self.__MAZE_MIN_Y, self.__MAZE_MAX_Y + 1):
                    # ステップを計算すべきマスがある
                    if self.__MAZE_GRIDS[x][y].g_step != None:
                        # 西(W)にいける場合の計算
                        if  x != self.__MAZE_MIN_X:
                            # ゴールの場合じゃないなら更新する
                            # 西の壁がないか、未探索
                            if      self.__MAZE_GRIDS[x - 1][y].g_step == None \
                                and (self.__MAZE_GRIDS[x][y].e_wall == False or self.__MAZE_GRIDS[x][y].e_wall == None):
                                self.__MAZE_GRIDS[x - 1][y].g_step = self.__MAZE_GRIDS[x][y].g_step + 1
                        # 東にいける
                        if  x != self.__MAZE_MAX_X:
                            # ゴールの場合じゃないなら更新する
                            # 東の壁がないか、未探索
                            if      self.__MAZE_GRIDS[x + 1][y].g_step == None \
                                and (self.__MAZE_GRIDS[x][y].w_wall == False or self.__MAZE_GRIDS[x][y].w_wall == None):
                                self.__MAZE_GRIDS[x + 1][y].g_step = self.__MAZE_GRIDS[x][y].g_step + 1

                        # 北にいける
                        if  y != self.__MAZE_MAX_Y:
                            # ゴールの場合じゃないなら更新する
                            # 北の壁がないか、未探索
                            if      self.__MAZE_GRIDS[x][y + 1].g_step == None \
                                and (self.__MAZE_GRIDS[x][y].n_wall == False or self.__MAZE_GRIDS[x][y].n_wall == None):
                                self.__MAZE_GRIDS[x][y + 1].g_step = self.__MAZE_GRIDS[x][y].g_step + 1

                        # 南にいける
                        if  y != self.__MAZE_MIN_Y:
                            # ゴールの場合じゃないなら更新する
                            # 南の壁がないか、未探索
                            if      self.__MAZE_GRIDS[x][y - 1].g_step == None \
                                and (self.__MAZE_GRIDS[x][y].s_wall == False or self.__MAZE_GRIDS[x][y].s_wall == None):
                                self.__MAZE_GRIDS[x][y - 1].g_step = self.__MAZE_GRIDS[x][y].g_step + 1
            loopContinue = False
            for x in range(self.__MAZE_MIN_X, self.__MAZE_MAX_X + 1):
                for y in range(self.__MAZE_MIN_Y, self.__MAZE_MAX_Y + 1):
                    if self.__MAZE_GRIDS[x][y].g_step == None:
                        loopContinue = True
            if (self.__MAZE_OCEAN * self.__MAZE_OCEAN) < cnt:
                break
            cnt += 1

        for x in range(self.__MAZE_MIN_X, self.__MAZE_MAX_X + 1):
            for y in range(self.__MAZE_MIN_Y, self.__MAZE_MAX_Y + 1):

                if      self.__MAZE_GRIDS[x][y].g_step > self.__MAZE_GRIDS[x + 1][y].g_step \
                    and self.__MAZE_GRIDS[x][y].w_wall != True :
                    # 東が空いてる
                    self.__MAZE_GRIDS[x][y].goal_way = self.Grid.WayFinding.WEST

                elif    self.__MAZE_GRIDS[x][y].g_step > self.__MAZE_GRIDS[x - 1][y].g_step \
                    and self.__MAZE_GRIDS[x][y].e_wall != True :
                    # 西が空いてる
                    self.__MAZE_GRIDS[x][y].goal_way = self.Grid.WayFinding.EAST

                elif    self.__MAZE_GRIDS[x][y].g_step > self.__MAZE_GRIDS[x][y + 1].g_step \
                    and self.__MAZE_GRIDS[x][y].n_wall != True :
                    # 北が空いてる
                    self.__MAZE_GRIDS[x][y].goal_way = self.Grid.WayFinding.NORTH
                elif    self.__MAZE_GRIDS[x][y].g_step > self.__MAZE_GRIDS[x][y - 1].g_step \
                    and self.__MAZE_GRIDS[x][y].s_wall != True :
                    # 南が空いてる
                    self.__MAZE_GRIDS[x][y].goal_way = self.Grid.WayFinding.SOUTH


    def real2maze(self, position:tuple[float, float, float],offset:tuple[float, float],  snsWalls:tuple[bool, bool, bool]) -> tuple[int, int, int, int, Optional[bool],Optional[bool],Optional[bool],Optional[bool]]:
        rfang = position[2]
        # 東向きの座標
        rfx = position[self.INDEX_X]
        srfx = rfx + offset[self.INDEX_X] * cos(radians(rfang)) + offset[self.INDEX_Y] * sin(radians(rfang))
        # 北向きの座標
        rfy = position[self.INDEX_Y]
        srfy = rfy + offset[self.INDEX_Y] * cos(radians(rfang)) - offset[self.INDEX_X] * sin(radians(rfang))
        sns_l = snsWalls[0]
        sns_f = snsWalls[1]
        sns_r = snsWalls[2]
        ix = floor(rfx / self.__MAZE_GRID_SIZE)
        iy = floor(rfy / self.__MAZE_GRID_SIZE)
        six = round(srfx / self.__MAZE_GRID_SIZE)
        siy = round(srfy / self.__MAZE_GRID_SIZE)
        tmps = (None, None, None, None)
        if (315.0 < rfang and rfang <= 360.0) or (0.0 <= rfang and rfang < 45.0):
            # 北向き
            # def checkwall(  self, position_xy=tuple[int,int], walls_nsew:tuple[Optional[bool], Optional[bool],Optional[bool],Optional[bool]] = (None, None, None, None)):
            tmps = (sns_f, None, sns_l, sns_r)
        elif (45.0 < rfang and rfang <= 135.0):
            # 東向き
            tmps = (sns_l, sns_r, None, sns_f)
        elif (135.0 < rfang and rfang <= 215.0):
            # 南向き
            tmps = (None, sns_f, sns_r, sns_l)
        elif (215.0 < rfang and rfang <= 315.0):
            # 西向き
            tmps = (sns_r, sns_l, sns_f, None)
        else:
            pass
        # walls_nse
        return (ix, iy, six, siy, tmps[0], tmps[1], tmps[2], tmps[3])
    
    def readStep(self, position:tuple[float, float, float]) -> tuple[int, int, int, int]:
        rfang = position[2]
        # 東向きの座標
        rfx = position[self.INDEX_X]
        # 北向きの座標
        rfy = position[self.INDEX_Y]
        ix = round(rfx / self.__MAZE_GRID_SIZE) + self.__MAZE_MIN_X
        iy = round(rfy / self.__MAZE_GRID_SIZE) + self.__MAZE_MIN_Y
        tmps = (None, None, None, None)
        nowstep = self.__MAZE_GRIDS[ix][iy].g_step
        if (315.0 < rfang and rfang <= 360.0) or (0.0 <= rfang and rfang < 45.0):
            # 北向き
            tmps = (nowstep, self.__MAZE_GRIDS[ix - 1][iy + 1].g_step, self.__MAZE_GRIDS[ix][iy + 1].g_step, self.__MAZE_GRIDS[ix + 1][iy + 1].g_step)
        elif (45.0 < rfang and rfang <= 135.0):
            # 東向き
            tmps = (nowstep, self.__MAZE_GRIDS[ix + 1][iy + 1].g_step, self.__MAZE_GRIDS[ix + 1][iy].g_step, self.__MAZE_GRIDS[ix + 1][iy - 1].g_step)
        elif (135.0 < rfang and rfang <= 215.0):
            # 南向き
            tmps = (nowstep, self.__MAZE_GRIDS[ix + 1][iy - 1].g_step, self.__MAZE_GRIDS[ix][iy -1].g_step, self.__MAZE_GRIDS[ix - 1][iy - 1].g_step)
        elif (215.0 < rfang and rfang <= 315.0):
            # 西向き
            tmps = (nowstep, self.__MAZE_GRIDS[ix - 1][iy - 1].g_step, self.__MAZE_GRIDS[ix - 1][iy].g_step, self.__MAZE_GRIDS[ix - 1][iy + 1].g_step)
        else:
            pass
        return tmps