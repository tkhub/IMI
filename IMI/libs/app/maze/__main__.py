from maze import Maze

def main():

    rx:float = 0.0
    ry:float = 0.0
    rdeg:float = 0.0
    offset_f = 89.9
    print("----------Init---------")
    cnt:int = 0    
    print(f"--------{cnt}--------")
    smallmaze = Maze(maze_size=(8,8), goal=(3,3))
    smallmaze.refreshStep()
    smallmaze.calcStep()
    smallmaze.show()
    cnt += 1

    # とりあえずスタートゲートから出る
    print(f"\n--------{cnt}--------")
    # センサで拾ってみる
    smallmaze.updateWall(   position_xy=(   0,    1), \
                            walls_nsew=(    False,  None,   True,  True))
    smallmaze.refreshStep()
    smallmaze.calcStep()
    smallmaze.show()
    cnt += 1

    # 北に進めと判断されたので北に進む
    print(f"\n--------{cnt}--------")
    # センサで拾ってみる
    smallmaze.updateWall(   position_xy=(   0,    2), \
                            walls_nsew=(    True,  None,   True,  False))
    smallmaze.refreshStep()
    smallmaze.calcStep()
    smallmaze.show()
    cnt += 1

    # 東に進めと判断されたので東に進む
    print(f"\n--------{cnt}--------")
    # センサで拾ってみる
    smallmaze.updateWall(   position_xy=(   1,    2), \
                            walls_nsew=(    True,   True,   None,  False))
    smallmaze.refreshStep()
    smallmaze.calcStep()
    smallmaze.show()
    cnt += 1

    # smallmaze = Maze(maze_size=(16,16), goal=(7,7))
    # smallmaze.updateWall(position_xy=(7,    7),     walls_nsew=(False,  True,   False,  False))
    # smallmaze.updateWall(position_xy=(8,    7),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(7,    8),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(8,    8),     walls_nsew=(True,   False,  False,  True))

    # smallmaze.updateWall(position_xy=(1,    0),     walls_nsew=(False,  True,   True,   False))
    # smallmaze.updateWall(position_xy=(3,    0),     walls_nsew=(False,  True,   True,   False))
    # smallmaze.updateWall(position_xy=(5,    0),     walls_nsew=(False,  True,   True,   False))
    # smallmaze.updateWall(position_xy=(7,    0),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(9,    0),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(11,   0),     walls_nsew=(False,  True,   False,  False))
    # smallmaze.updateWall(position_xy=(13,   0),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(15,   0),     walls_nsew=(False,  True,   False,  True))

    # smallmaze.updateWall(position_xy=(0,    1),     walls_nsew=(False,  False,  True,   False))
    # smallmaze.updateWall(position_xy=(2,    1),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(4,    1),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(6,    1),     walls_nsew=(True,   True,   True,   False))
    # smallmaze.updateWall(position_xy=(8,    1),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(10,   1),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(12,   1),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(14,   1),     walls_nsew=(False,  False,  True,   True))

    # smallmaze.updateWall(position_xy=(1,    2),     walls_nsew=(False,  True,   False,  False))
    # smallmaze.updateWall(position_xy=(3,    2),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(5,    2),     walls_nsew=(True,   False,  False,  False))
    # smallmaze.updateWall(position_xy=(7,    2),     walls_nsew=(True,   False,  False,  True))
    # smallmaze.updateWall(position_xy=(9,    2),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(11,   2),     walls_nsew=(False,  False,  False,  True))
    # smallmaze.updateWall(position_xy=(13,   2),     walls_nsew=(True,   False,  False,  True))
    # smallmaze.updateWall(position_xy=(15,   2),     walls_nsew=(False,  False,  True,   True))

    # smallmaze.updateWall(position_xy=(0,    3),     walls_nsew=(True,   True,   True,   False))
    # smallmaze.updateWall(position_xy=(2,    3),     walls_nsew=(True,   True,   False,  True))
    # smallmaze.updateWall(position_xy=(4,    3),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(6,    3),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(8,    3),     walls_nsew=(True,   False,  False,  True))
    # smallmaze.updateWall(position_xy=(10,   3),     walls_nsew=(False,  False,  False,  True))
    # smallmaze.updateWall(position_xy=(12,   3),     walls_nsew=(True,   False,  False,  True))
    # smallmaze.updateWall(position_xy=(14,   3),     walls_nsew=(True,   False,  False,  True))

    # smallmaze.updateWall(position_xy=(1,    4),     walls_nsew=(False,  False,  False,  False))
    # smallmaze.updateWall(position_xy=(3,    4),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(5,    4),     walls_nsew=(False,  False,  True,   False))
    # smallmaze.updateWall(position_xy=(7,    4),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(9,    4),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(11,   4),     walls_nsew=(True,   False,  False,  True))
    # smallmaze.updateWall(position_xy=(13,   4),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(15,   4),     walls_nsew=(False,  False,  True,   True))


    # smallmaze.updateWall(position_xy=(0,    5),     walls_nsew=(True,   True,   True,   False))
    # smallmaze.updateWall(position_xy=(2,    5),     walls_nsew=(True,   True,   False,  True))
    # smallmaze.updateWall(position_xy=(4,    5),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(6,    5),     walls_nsew=(False,  True,   True,   False))
    # smallmaze.updateWall(position_xy=(8,    5),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(10,   5),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(12,   5),     walls_nsew=(False,  False,  False,  True))
    # smallmaze.updateWall(position_xy=(14,   5),     walls_nsew=(False,  False,  False,  True))

    # smallmaze.updateWall(position_xy=(1,    6),     walls_nsew=(True,   False,  False,  False))
    # smallmaze.updateWall(position_xy=(3,    6),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(5,    6),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(7,    6),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(9,    6),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(11,   6),     walls_nsew=(True,   False,  False,  True))
    # smallmaze.updateWall(position_xy=(13,   6),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(15,   6),     walls_nsew=(False,  False,  True,   True))

    # smallmaze.updateWall(position_xy=(0,    7),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(2,    7),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(4,    7),     walls_nsew=(True,   False,  True,   True))
    # smallmaze.updateWall(position_xy=(6,    7),     walls_nsew=(False,  False,  True,   False))
    # smallmaze.updateWall(position_xy=(8,    7),     walls_nsew=(None,   None,   None,   None))
    # smallmaze.updateWall(position_xy=(10,   7),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(12,   7),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(14,   7),     walls_nsew=(False,  False,  True,   True))

    # smallmaze.updateWall(position_xy=(1,    8),     walls_nsew=(False,  False,  True,   False))
    # smallmaze.updateWall(position_xy=(3,    8),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(5,    8),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(7,    8),     walls_nsew=(None,   None,   None,   None))
    # smallmaze.updateWall(position_xy=(9,    8),     walls_nsew=(False,  False,  True,   False))
    # smallmaze.updateWall(position_xy=(11,   8),     walls_nsew=(True,   False,  False,  False))
    # smallmaze.updateWall(position_xy=(13,   8),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(15,   8),     walls_nsew=(False,  False,  True,   True))

    # smallmaze.updateWall(position_xy=(0,    9),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(2,    9),     walls_nsew=(False,  False,  True,   False))
    # smallmaze.updateWall(position_xy=(4,    9),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(6,    9),     walls_nsew=(False,  True,   True,   True))
    # smallmaze.updateWall(position_xy=(8,    9),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(10,   9),     walls_nsew=(False,  True,   False,  False))
    # smallmaze.updateWall(position_xy=(12,   9),     walls_nsew=(True,   False,  False,  False))
    # smallmaze.updateWall(position_xy=(14,   9),     walls_nsew=(False,  False,  True,   True))

    # smallmaze.updateWall(position_xy=(1,   10),     walls_nsew=(True,   False,  False,  True))
    # smallmaze.updateWall(position_xy=(3,   10),     walls_nsew=(False,  True,   True,   False))
    # smallmaze.updateWall(position_xy=(5,   10),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(7,   10),     walls_nsew=(True,   False,  False,  True))
    # smallmaze.updateWall(position_xy=(9,   10),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(11,  10),     walls_nsew=(False,  True,   True,   False))
    # smallmaze.updateWall(position_xy=(13,  10),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(15,  10),     walls_nsew=(False,  False,  True,   True))

    # smallmaze.updateWall(position_xy=(0,   11),     walls_nsew=(False,  True,   True,   False))
    # smallmaze.updateWall(position_xy=(2,   11),     walls_nsew=(True,   False,  False,  True))
    # smallmaze.updateWall(position_xy=(4,   11),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(6,   11),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(8,   11),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(10,  11),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(12,  11),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(14,  11),     walls_nsew=(False,  False,  False,  True))

    # smallmaze.updateWall(position_xy=(1,   12),     walls_nsew=(False,  True,   True,   False))
    # smallmaze.updateWall(position_xy=(3,   12),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(5,   12),     walls_nsew=(False,  False,  True,   True))
    # smallmaze.updateWall(position_xy=(7,   12),     walls_nsew=(False,  False,  False,  True))
    # smallmaze.updateWall(position_xy=(9,   12),     walls_nsew=(False,  False,  False,  True))
    # smallmaze.updateWall(position_xy=(11,  12),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(13,  12),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(15,  12),     walls_nsew=(False,  False,  True,   True))

    # smallmaze.updateWall(position_xy=(0,   13),     walls_nsew=(False,  False,  True,   False))
    # smallmaze.updateWall(position_xy=(2,   13),     walls_nsew=(False,  True,   True,   False))
    # smallmaze.updateWall(position_xy=(4,   13),     walls_nsew=(False,  True,   True,   False))
    # smallmaze.updateWall(position_xy=(6,   13),     walls_nsew=(True,   False,  True,   True))
    # smallmaze.updateWall(position_xy=(8,   13),     walls_nsew=(True,   False,  False,  True))
    # smallmaze.updateWall(position_xy=(10,  13),     walls_nsew=(True,   False,  False,  True))
    # smallmaze.updateWall(position_xy=(12,  13),     walls_nsew=(False,  True,   False,  True))
    # smallmaze.updateWall(position_xy=(14,  13),     walls_nsew=(False,  True,   False,  True))

    # smallmaze.updateWall(position_xy=(1,   14),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(3,   14),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(5,   14),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(7,   14),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(9,   14),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(11,  14),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(13,  14),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(15,  14),     walls_nsew=(False,  False,  False,  True))
    
    # smallmaze.updateWall(position_xy=(0,   15),     walls_nsew=(True,   False,  True,   False))
    # smallmaze.updateWall(position_xy=(2,   15),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(4,   15),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(6,   15),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(8,   15),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(10,  15),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(12,  15),     walls_nsew=(True,   True,   False,  False))
    # smallmaze.updateWall(position_xy=(14,  15),     walls_nsew=(True,   True,   False,  False))

    # smallmaze.refreshStep()
    # smallmaze.calcStep()
    # smallmaze.show()


    # y=1,x=0の壁をチェックする
    # 壁の状態を変換してかきこむ
    # 再度ステップを計算する
    # 次に行くべき場所を確認する
    # print(f"\n--------{cnt}--------") # 90 mm 前に進んで際に行く
    # ry += 90
    # print(f"rx = {rx}, ry = {ry}, rdeg = {rdeg}")
    # mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    # smallmaze.updateWall(position_xy=(mazedat[2], mazedat[3]) ,walls_nsew=mazedat[4:])
    # smallmaze.refreshStep()
    # smallmaze.calcStep()
    # print(smallmaze.readStep(position=(0, 0, rdeg)))
    # smallmaze.show()
    # cnt += 1

    
    # print(f"step={cnt}, rx = {rx}, ry = {ry}, rdeg = {rdeg}")
    # mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0,0), snsWalls=(True, False, True))


    # ry += 180
    # print(f"rx = {rx}, ry = {ry}, rdeg = {rdeg}")
    # mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    # print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[4]},{mazedat[5]},{mazedat[6]},{mazedat[7]})")
    # smallmaze.checkwall(position_xy=(mazedat[2], mazedat[3]) ,walls_nsew=mazedat[4:])
    # smallmaze.refreshStep()
    # smallmaze.calcStep()
    # print(smallmaze.readStep(position=(rx, ry, rdeg)))
    # print(f"(3,4)はサーチ済み?={smallmaze.isReached((3, 4))}")
    # print(f"(0,1)はサーチ済み?={smallmaze.isReached((0, 1))}")
    # print(f"(0,0)はサーチ済み?={smallmaze.isReached((0, 0))}")
    # smallmaze.show()
    # cnt += 1

    # ry += 90.02
    # rdeg += 90
    # rx += 90
    # print(f"rx = {rx}, ry = {ry}, rdeg = {rdeg}")
    # mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    # print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[4]},{mazedat[5]},{mazedat[6]},{mazedat[7]})")
    # smallmaze.checkwall(position_xy=(mazedat[2], mazedat[3]) ,walls_nsew=mazedat[4:])
    # smallmaze.refreshStep()
    # smallmaze.calcStep()
    # print(smallmaze.readStep(position=(rx, ry, rdeg)))
    # smallmaze.show()
    # cnt += 1


    # # print(f"\n--------{cnt}--------")
    # # ry += 180
    # # print("90mm GO")
    # # mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    # # print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[2]},{mazedat[3]},{mazedat[4]},{mazedat[5]})")
    # # print(smallmaze.readStep(position=(rx, ry, rdeg), offset=(0, 90)))
    # # smallmaze.checkwall(position_xy=mazedat[:2], walls_nsew=mazedat[2:])
    # # smallmaze.refreshStep()
    # # smallmaze.calcStep()
    # # smallmaze.show()
    # # cnt += 1

    # # print(f"\n--------{cnt}--------")
    # # ry += 180
    # # print("180mm GO")
    # # mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    # # print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[2]},{mazedat[3]},{mazedat[4]},{mazedat[5]})")
    # # print(smallmaze.readStep(position=(rx, ry, rdeg), offset=(0, 90)))
    # # smallmaze.checkwall(position_xy=mazedat[:2], walls_nsew=mazedat[2:])
    # # smallmaze.refreshStep()
    # # smallmaze.calcStep()
    # # smallmaze.show()
    # # cnt += 1

    # # print(f"\n--------{cnt}--------")
    # # ry += 90
    # # rdeg += 90
    # # rx += 90
    # # print("+90 Trun GO")
    # # mazedat = smallmaze.real2maze(position=(rx, ry, rdeg), offset=(0, offset_f), snsWalls=(True, False, True))
    # # print(f"x = {mazedat[0]}, y = {mazedat[1]}, walls = ({mazedat[2]},{mazedat[3]},{mazedat[4]},{mazedat[5]})")
    # # print(smallmaze.readStep(position=(rx, ry, rdeg), offset=(0, 90)))
    # # smallmaze.checkwall(position_xy=mazedat[:2], walls_nsew=mazedat[2:])
    # # smallmaze.refreshStep()
    # # smallmaze.calcStep()
    # # smallmaze.show()
    # # cnt += 1

if __name__ == '__main__':
    main()