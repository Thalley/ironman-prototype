#Adapter for HomePort
#Implements functions to provide abstraction for the server
import httplib
import mapper
import xml.etree.ElementTree

#Assuming HomePort is run on same machine on port 8888
CONNECTION =  httplib.HTTPConnection('localhost:8888')

#Returns HomePort devices as a list of device objects
def request_homeport_devices():
    # CONNECTION.request('GET', '/devices')
    # result = CONNECTION.getresponse()
    # e = xml.etree.ElementTree.parse('./homeport.xml')
    #TODO: Do something about the result 

    # Hardcoded devices (for now)
    device1 = Device(0, 'Lamp at Couches', (6.50, 3.35), ['turnOn', 'turnOff'], '/phidget/173111/output/0')
    device2 = Device(1, 'Lamp at Dinner Table', (2.68, 1.92), ['turnOn', 'turnOff'], '/phidget/173111/output/1')
    devices = [device1, device2]
    result devices

#Performs an action on a HomePort device
def do_homeport_action(device, action):
    body_content = "<?xml version='1.0' encoding='UTF-8'?>value>" + mapper.map_action_to_id(action) + "</value>"
    connection.request('PUT', device.url, body_content)
    result = connection.getresponse()

request_homeport_devices()