import asyncio
from kasa import SmartBulb

async def main():
    p = SmartBulb("192.168.2.94")

    await p.update()  # Request the update
    print(p.alias)  # Print out the alias
    #print(p.emeter_realtime)  # Print out current emeter status

    #await p.turn_off()  # Turn the device off
    await p.set_hsv(345,100,20)

if __name__ == "__main__":
    asyncio.run(main())