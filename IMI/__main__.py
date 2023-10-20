import sys
import time

def main():
    while True:
        print("Hello!")
        time.sleep(10)


if __name__ == "__main__":
    try :
        main()
    except KeyboardInterrupt:
        print("Exit")
        sys.exit()