import paho.mqtt.client as mqtt
import asyncio,json 
from kasa import Discover, Credentials, SmartBulb, SmartPlug

devip=dict()
devtype=dict()

async def discover():
    
    global devip
    global devtype
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
        #if devtype[alias]=="Bulb": await setbulb(devip[alias]) 
        #if devtype[alias]=="Plug": await setplug(devip[alias])
 
async def setbulb(ip,bri):
    p = SmartBulb(ip)

    await p.update()  # Request the update
    #print(p.alias)  # Print out the alias
    #print(p.emeter_realtime)  # Print out current emeter status

    #await p.turn_off()  # Turn the device off
    #await p.set_hsv(0,100,int(bri/2.55))
    await p.set_brightness(int(bri/2.55))

async def onbulb(ip,on):
    p = SmartBulb(ip)

    await p.update()  # Request the update
    #print(p.alias)  # Print out the alias
    #print(p.emeter_realtime)  # Print out current emeter status

    if on: await p.turn_on()  # Turn the device on
    else: await p.turn_off()  # Turn the device off
    #await p.set_hsv(0,100,bri/2.55)

async def setplug(ip,on):
    p = SmartPlug(ip)

    await p.update()  # Request the update
    #print(p.alias)  # Print out the alias
    #print(p.emeter_realtime)  # Print out current emeter status

    if on: await p.turn_on()  # Turn the device on
    else: await p.turn_off()  # Turn the device off


asyncio.run(discover())

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("mqttkasa/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global devip
    global devtype
    try:
        s1=bytes(msg.payload).decode()
        d1 = json.loads(s1)
        target=msg.topic[9:]
        print(msg.topic+" "+msg.topic[9:]+" "+s1,devtype[target])
        if devtype[target] == 'Bulb':
          if 'bri' in d1.keys(): asyncio.run(setbulb(devip[target],d1['bri']))
          if 'on' in d1.keys(): asyncio.run(onbulb(devip[target],d1['on']))
        else:
          asyncio.run(setplug(devip[target],d1['on']))
    except:
        print("error occured")


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("192.168.2.82", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()
