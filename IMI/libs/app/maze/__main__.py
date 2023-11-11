from maze import Maze

def main():

    rx:float = 89.99
    ry:float = 89.99
    rdeg:float = 0.0
    offset_f = 89
    print("----------Init---------")
    cnt:int = 0    
    print(f"--------{cnt}--------")
    smallmaze = Maze(maze_size=(6,6), goal=(3,3))
    smallmaze.refreshStep()
    smallmaze.calcStep()
    smallmaze.show()
    cnt += 1

    # 90 mm 前に進んで際に行く
    # y=1,x=0の壁をチェックする
    # 壁の状態を変換してかきこむ
    # 再度ステップを計算する
    # 次に行くべき場所を確認する
    ry += 90
    print(f"rx = {rx}, ry = {ry}, rdeg = {rdeg}")
    mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[4]},{mazedat[5]},{mazedat[6]},{mazedat[7]})")
    smallmaze.checkwall(position_xy=(mazedat[2], mazedat[3]) ,walls_nsew=mazedat[4:])
    smallmaze.refreshStep()
    smallmaze.calcStep()
    print(smallmaze.readStep(position=(0, 0, rdeg)))
    smallmaze.show()
    cnt += 1


    ry += 180
    print(f"rx = {rx}, ry = {ry}, rdeg = {rdeg}")
    mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[4]},{mazedat[5]},{mazedat[6]},{mazedat[7]})")
    smallmaze.checkwall(position_xy=(mazedat[2], mazedat[3]) ,walls_nsew=mazedat[4:])
    smallmaze.refreshStep()
    smallmaze.calcStep()
    print(smallmaze.readStep(position=(rx, ry, rdeg)))
    smallmaze.show()
    cnt += 1

    ry += 90.02
    rdeg += 90
    rx += 90
    print(f"rx = {rx}, ry = {ry}, rdeg = {rdeg}")
    mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[4]},{mazedat[5]},{mazedat[6]},{mazedat[7]})")
    smallmaze.checkwall(position_xy=(mazedat[2], mazedat[3]) ,walls_nsew=mazedat[4:])
    smallmaze.refreshStep()
    smallmaze.calcStep()
    print(smallmaze.readStep(position=(rx, ry, rdeg)))
    smallmaze.show()
    cnt += 1


    # print(f"\n--------{cnt}--------")
    # ry += 180
    # print("90mm GO")
    # mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    # print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[2]},{mazedat[3]},{mazedat[4]},{mazedat[5]})")
    # print(smallmaze.readStep(position=(rx, ry, rdeg), offset=(0, 90)))
    # smallmaze.checkwall(position_xy=mazedat[:2], walls_nsew=mazedat[2:])
    # smallmaze.refreshStep()
    # smallmaze.calcStep()
    # smallmaze.show()
    # cnt += 1

    # print(f"\n--------{cnt}--------")
    # ry += 180
    # print("180mm GO")
    # mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    # print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[2]},{mazedat[3]},{mazedat[4]},{mazedat[5]})")
    # print(smallmaze.readStep(position=(rx, ry, rdeg), offset=(0, 90)))
    # smallmaze.checkwall(position_xy=mazedat[:2], walls_nsew=mazedat[2:])
    # smallmaze.refreshStep()
    # smallmaze.calcStep()
    # smallmaze.show()
    # cnt += 1

    # print(f"\n--------{cnt}--------")
    # ry += 90
    # rdeg += 90
    # rx += 90
    # print("+90 Trun GO")
    # mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    # print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[2]},{mazedat[3]},{mazedat[4]},{mazedat[5]})")
    # print(smallmaze.readStep(position=(rx, ry, rdeg), offset=(0, 90)))
    # smallmaze.checkwall(position_xy=mazedat[:2], walls_nsew=mazedat[2:])
    # smallmaze.refreshStep()
    # smallmaze.calcStep()
    # smallmaze.show()
    # cnt += 1

if __name__ == '__main__':
    main()