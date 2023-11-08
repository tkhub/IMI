from typing import Optional
from enum import Enum
class Maze:
    class Grid:
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

    __GOAL_SIZE_X :int = 2
    __GOAL_SIZE_Y :int = 2
    __GOAL_POSITION_X:int
    __GOAL_POSITION_Y:int
    __MAZE_SIZE_X :int
    __MAZE_SIZE_Y :int
    def __init__(self, maze_size:(int,int), goal:(int, int)) -> None:
        self.__MAZE_SIZE_X = maze_size[0]
        self.__MAZE_SIZE_Y = maze_size[1]
        self.__GOAL_POSITION_X = goal[0]
        self.__GOAL_POSITION_Y = goal[1]
        tmpmaze = self.Grid()
        tmpmaze.n_wall = None
        tmpmaze.s_wall = None
        tmpmaze.w_wall = None
        tmpmaze.e_wall = None
        tmpmaze.g_step = None
        tmpmaze.goal_way = tmpmaze.WayFinding.NOWAY
        # self.__MAZE_GRIDS = [[self.Grid() for x in range(self.__MAZE_SIZE_X)] for y in range(self.__MAZE_SIZE_Y)]
        self.__MAZE_GRIDS = [[self.Grid() for y in range(self.__MAZE_SIZE_Y)] for x in range(self.__MAZE_SIZE_X)]
        for x in range(self.__MAZE_SIZE_X):
            self.__MAZE_GRIDS[x][0].s_wall = True
            self.__MAZE_GRIDS[x][self.__MAZE_SIZE_Y - 1].n_wall = True
        for y in range(self.__MAZE_SIZE_Y):
            self.__MAZE_GRIDS[0][y].e_wall = True
            self.__MAZE_GRIDS[self.__MAZE_SIZE_X - 1][y].w_wall = True

    def __isGoal(self, position:(int,int)) -> bool:
        if      (   self.__GOAL_POSITION_X == position[0] \
            or      self.__GOAL_POSITION_X == (position[0] + 1)) \
            and (   self.__GOAL_POSITION_Y == position[1] \
            or      self.__GOAL_POSITION_Y == (position[1] + 1)):
            return True
        else:
            return False

    def checkwall(self, position=(int,int), nwall:Optional[bool] = None, \
                  wwall:Optional[bool] = None, ewall:Optional[bool] = None, swall:Optional[bool] = None):
        if nwall == True:
            self.__MAZE_GRIDS[position[0]][position[1]].n_wall = True
            if position[1] != self.__MAZE_SIZE_Y - 1:
                self.__MAZE_GRIDS[position[0]][position[1]+1].s_wall = True
        elif nwall == False:
            self.__MAZE_GRIDS[position[0]][position[1]].n_wall = False

        if swall == True:
            self.__MAZE_GRIDS[position[0]][position[1]].s_wall = True
            if position[1] != 0:
                self.__MAZE_GRIDS[position[0]][position[1]-1].n_wall = True
        elif swall == False:
            self.__MAZE_GRIDS[position[0]][position[1]].s_wall = False

        if ewall == True:
            self.__MAZE_GRIDS[position[0]][position[1]].e_wall = True
            if position[0] != 0:
                self.__MAZE_GRIDS[position[0]-1][position[1]].w_wall = True
        elif ewall == False:
            self.__MAZE_GRIDS[position[0]][position[1]].e_wall = False

        if wwall == True:
            self.__MAZE_GRIDS[position[0]][position[1]].w_wall = True
            if position[0] != self.__MAZE_SIZE_X - 1:
                self.__MAZE_GRIDS[position[0]+1][position[1]].e_wall = True
        elif wwall == False:
            self.__MAZE_GRIDS[position[0]][position[1]].w_wall = False


    def show(self) :
        mazestrH:str
        mazestrM:str
        mazestrL:str
        num:int
        yi:int
        for y in range(self.__MAZE_SIZE_Y):
            yi = self.__MAZE_SIZE_Y - y - 1
            mazestrH =" \t"
            mazestrM = str(yi) + " \t"
            mazestrL =" \t"
            for x in range(self.__MAZE_SIZE_X):
                if self.__MAZE_GRIDS[x][yi].n_wall == True:
                    mazestrH += "+-------+"
                else:
                    mazestrH += "+       +"
                if self.__MAZE_GRIDS[x][yi].e_wall == True:
                    mazestrM += "|"
                else :
                    mazestrM += " "
                # フラグ表示
                if self.__isGoal((x,yi)) == True:
                    mazestrM += " G"
                elif x == 0 and yi == 0:
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

                if self.__MAZE_GRIDS[x][yi].g_step != None:
                    
                    mazestrM += str(self.__MAZE_GRIDS[x][yi].g_step).rjust(4) + " "
                else:
                    mazestrM += ".... "
                
                if self.__MAZE_GRIDS[x][yi].w_wall == True:
                    mazestrM += "|"
                else:
                    mazestrM += " "

                if self.__MAZE_GRIDS[x][yi].s_wall == True:
                    mazestrL += "+-------+"
                else:
                    mazestrL += "+       +"
            print(mazestrH)
            print(mazestrM)
            print(mazestrL)
        mazestrH =" \t"
        for x in range(self.__MAZE_SIZE_X):
            mazestrH += "    " + str(x) + "    "
        print(mazestrH)

