from maze import Maze

def main():

    rx:float = 0.0
    ry:float = 0.0
    rdeg:float = 0.0
    offset_f = 90
    print("----------Init---------")
    cnt:int = 0    
    print(f"--------{cnt}--------")
    smallmaze = Maze(maze_size=(6,6), goal=(3,3))
    smallmaze.refreshStep()
    smallmaze.calcStep()
    smallmaze.show()
    cnt += 1    

    print(f"\n--------{cnt}--------")
    ry += 90
    print("90mm GO")
    mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[2]},{mazedat[3]},{mazedat[4]},{mazedat[5]})")
    print(smallmaze.readStep(position=(rx, ry, rdeg), offset=(0, 90)))
    smallmaze.checkwall(position_xy=mazedat[:2], walls_nsew=mazedat[2:])
    smallmaze.refreshStep()
    smallmaze.calcStep()
    smallmaze.show()
    cnt += 1    

    print(f"\n--------{cnt}--------")
    ry += 180
    print("180mm GO")
    mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[2]},{mazedat[3]},{mazedat[4]},{mazedat[5]})")
    print(smallmaze.readStep(position=(rx, ry, rdeg), offset=(0, 90)))
    smallmaze.checkwall(position_xy=mazedat[:2], walls_nsew=mazedat[2:])
    smallmaze.refreshStep()
    smallmaze.calcStep()
    smallmaze.show()
    cnt += 1    

    print(f"\n--------{cnt}--------")
    ry += 90
    print("90mm GO")
    mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, False))
    print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[2]},{mazedat[3]},{mazedat[4]},{mazedat[5]})")
    print(smallmaze.readStep(position=(rx, ry, rdeg), offset=(0, 90)))
    smallmaze.checkwall(position_xy=mazedat[:2], walls_nsew=mazedat[2:])
    smallmaze.refreshStep()
    smallmaze.calcStep()
    smallmaze.show()
    cnt += 1    


if __name__ == '__main__':
    main()