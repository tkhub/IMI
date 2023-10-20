import spidev
from mcp3XXX import MCP3XXX

def main():
    spi = MCP3XXX(0,chnum = 8)
    print("MCP3XXX module")
    print(spi.read())
    spi.close()

if __name__ == "__main__":
    main()