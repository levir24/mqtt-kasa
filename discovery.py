import asyncio
from kasa import Discover, Credentials, SmartBulb, SmartPlug

async def setbulb(ip):
    p = SmartBulb(ip)

    await p.update()  # Request the update
    print(p.alias)  # Print out the alias
    #print(p.emeter_realtime)  # Print out current emeter status

    #await p.turn_off()  # Turn the device off
    await p.set_hsv(345,100,20)

async def setplug(ip):
    p = SmartPlug(ip)

    await p.update()  # Request the update
    print(p.alias)  # Print out the alias
    #print(p.emeter_realtime)  # Print out current emeter status

    await p.turn_off()  # Turn the device off


async def main():
    
    """
    device = await Discover.discover_single(
        "127.0.0.1",
        credentials=Credentials("myusername", "mypassword"),
        discovery_timeout=10
    )

    await device.update()  # Request the update
    print(device.alias)  # Print out the alias
    """
    devip=dict()
    devtype=dict()
    devices = await Discover.discover(
        credentials=Credentials("myusername", "mypassword"),
        discovery_timeout=10
    )
    for ip, device in devices.items():
        await device.update()
        alias=device.alias.replace(" ", "_")
        print(ip,alias,device.device_type)
        devip[alias]=ip
        devtype[alias]=str(device.device_type).split(".")[1]
        if devtype[alias]=="Bulb": await setbulb(devip[alias]) 
        if devtype[alias]=="Plug": await setplug(devip[alias])

    #print (devip)
    #print (devtype)
     


if __name__ == "__main__":
    asyncio.run(main())