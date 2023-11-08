from maze import Maze

def main():
    testmaze = Maze(maze_size=(8,8), goal=(4,4))
    testmaze.show()
    testmaze.checkwall(position=(0,0), wwall=True)
    testmaze.checkwall(position=(0,1), wwall=True)
    testmaze.checkwall(position=(0,2), wwall=True)
    testmaze.checkwall(position=(0,3), nwall=True)
    testmaze.checkwall(position=(0,5), wwall=True)
    testmaze.checkwall(position=(0,6), wwall=True)

    testmaze.checkwall(position=(1,0), wwall=True)
    testmaze.checkwall(position=(1,1), wwall=True)
    testmaze.checkwall(position=(1,2), wwall=True)
    testmaze.checkwall(position=(1,3), nwall=True)
    testmaze.checkwall(position=(1,5), nwall=True, wwall=True)

    testmaze.checkwall(position=(2,1), swall=True)
    testmaze.checkwall(position=(2,2), wwall=True)
    testmaze.checkwall(position=(2,3), nwall=True, wwall=True)
    testmaze.checkwall(position=(2,4), wwall=True)
    testmaze.checkwall(position=(2,7), swall=True)

    testmaze.checkwall(position=(3,1), swall=True,wwall=True)
    testmaze.checkwall(position=(3,2), nwall=True)
    testmaze.checkwall(position=(3,6), swall=True)
    testmaze.checkwall(position=(3,7), swall=True)

    testmaze.checkwall(position=(4,1), wwall=True)
    testmaze.checkwall(position=(4,2), nwall=True,wwall=True)
    testmaze.checkwall(position=(4,5), swall=True)
    testmaze.checkwall(position=(4,7), swall=True)

    testmaze.checkwall(position=(5,0), nwall=True)
    testmaze.checkwall(position=(5,1), nwall=True)
    testmaze.checkwall(position=(5,2), nwall=True)
    testmaze.checkwall(position=(5,3), ewall=True, nwall=True)
    testmaze.checkwall(position=(5,4), ewall=True, nwall=True)
    testmaze.checkwall(position=(5,5), ewall=True, nwall=True)
    testmaze.checkwall(position=(5,6), ewall=True, nwall=True)

    testmaze.checkwall(position=(6,1), wwall=True)
    testmaze.checkwall(position=(6,2), wwall=True)
    testmaze.checkwall(position=(6,4), nwall=True, wwall=True)
    testmaze.checkwall(position=(6,6), nwall=True, wwall=True)

    testmaze.checkwall(position=(7,0), nwall=True)

    testmaze.show()
    

if __name__ == '__main__':
    main()