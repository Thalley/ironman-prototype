#Adapter for HomePort
#Implements functions to provide abstraction for the server
import httplib
import mapper
from device import Device

#Assuming HomePort is run on same machine on port 8888
HOSTNAME = 'localhost:8888' 

#Returns HomePort devices as a list of device objects
def request_homeport_devices():
    # Hardcoded devices (for now)
    device1 = Device(0, 'Lamp at Couches', (6.50, 3.35), ['turnOn', 'turnOff'], '/phidget/173111/output/0')
    device2 = Device(1, 'Lamp at Dinner Table', (2.68, 1.92), ['turnOn', 'turnOff'], '/phidget/173111/output/1')
    devices = [device1, device2]
    return devices

#Performs an action on a HomePort device
def do_homeport_action(device_id, action):
    connection =  httplib.HTTPConnection(HOSTNAME)
    body_content = "<?xml version='1.0' encoding='UTF-8'?><value>" + mapper.map_action_to_id(action) + "</value>"
    connection.request('PUT', '/phidget/173111/output/' + device_id, body_content)
    result = connection.getresponse()
    return result.status
