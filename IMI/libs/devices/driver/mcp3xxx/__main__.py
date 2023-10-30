import sys
import time
from mcp3xxx import MCP3XXX

def main():
    spi = MCP3XXX(0,chnum = 8)
    while True:
        print("MCP3XXX module")
        print(spi.read())
        time.sleep(0.1)
    spi.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()