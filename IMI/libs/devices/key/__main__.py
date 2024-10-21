import key
import pigpio
from time import sleep

def main():
    testpi = pigpio.pi()
    # UIKey = key.KeyPolling(pi = testpi)
    UIKeyE = key.KeyEvent(pi = testpi)
    try:
        while True:
            update, exitf, swstate = UIKeyE.detector() 
            if update:
                if not exitf:
                    print(f"state = {swstate}")
                else:
                    print("EXIT")
            sleep(0.01)

    except KeyboardInterrupt:
        print("Ctrl + C is Input")
    finally:
        # UIKey.close()
        UIKeyE.close()

if __name__ == '__main__':
    main()