#Adapter for HomePort
#Implements functions to provide abstraction for the server
import httplib
import mapper
from device import Device

#Assuming HomePort is run on same machine on port 8888
HOSTNAME = 'localhost:8888' 

# Hardcoded devices (for now)
device1 = Device(0, 'Lamp at Couches', (6.50, 3.35), ['turnOn', 'turnOff'], '/phidget/173111/output/0')
device2 = Device(1, 'Lamp at Dinner Table', (2.68, 1.92), ['turnOn', 'turnOff'], '/phidget/173111/output/1')
devices = [device1, device2]

#Returns HomePort devices as a list of device objects
def request_homeport_devices():
    return devices

#Performs an action on a HomePort device
#Returns HomePort response code
def do_homeport_action(device, action):
    #Create connection and setup request
    connection =  httplib.HTTPConnection(HOSTNAME)
    body_content = "<?xml version='1.0' encoding='UTF-8'?><value>" + mapper.map_action_to_id(action) + "</value>"
    connection.request('PUT', device.url, body_content)

    result = connection.getresponse()

    #If result is good, change state of device
    if (result.status == 200):
        for dev in devices:
            if (device.id == dev.id):
                dev.performAction(action)
                break
    return result.status
