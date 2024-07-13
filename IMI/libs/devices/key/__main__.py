import key
from time import sleep

def main():
    UIKey = key.Key()
    try:
        while True:
            SW = UIKey.detector() 
            if SW != key.UISWCmd.NON_SW_EVNT:
                print(f"return\t= {SW}")
            sleep(0.05)

    except KeyboardInterrupt:
        print("Ctrl + C is Input")
    finally:
        UIKey.close()

if __name__ == '__main__':
    main()