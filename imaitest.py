from time import sleep
from IMI.uisystem import UiSystem

def main():
    uisystem = UiSystem()
    sleep(5)
    uisystem.close()

if __name__ == '__main__':
    main()