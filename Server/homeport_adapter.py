#Adapter for HomePort
#Implements functions to provide abstraction for the server
import httplib
import mapper
import xml.etree.ElementTree as ET
from device import Device

#Assuming HomePort is run on same machine on port 8888
HOSTNAME = 'localhost:8888' 

# Hardcoded devices (for now)
# device1 = Device(0, 'Lamp at Couches', (6.50, 3.35), ['turnOn', 'turnOff'], '/phidget/173111/output/0')
# device2 = Device(1, 'Lamp at Dinner Table', (2.68, 1.92), ['turnOn', 'turnOff'], '/phidget/173111/output/1')
# devices = [device1, device2]


#Returns HomePort devices as a list of device objects
def request_homeport_devices():
    connection =  httplib.HTTPConnection(HOSTNAME)
    connection.request('GET', '/devices')
    xml_response = connection.getresponse()
    if(xml_response.status == 200):
        return __get_devices_from_xml(xml_response.read())
    else: 
        return xml_response #returns the erroneous response 



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

def __get_devices_from_xml(xml):
    root = ET.fromstring(xml)
    services = root.findall('.//service[@type="output"]')
    devices = []

    #Names and coords are still hardcoded for now
    for i in range(len(services)):
        if i == 0:
            devices.append(Device(services[i].attrib['id'], 
                                  'Lamp at Couches', \
                                  (6.50, 3.35), \
                                  __get_actions_from_xml(services[i].attrib['unit']), \
                                  services[i].attrib['value_url']))
        elif i == 1:
            devices.append(Device(services[i].attrib['id'], 
                                  'Lamp at Dinner Table', \
                                  (2.68, 1.92), \
                                  __get_actions_from_xml(services[i].attrib['unit']), \
                                  services[i].attrib['value_url']))
    return devices

# Homeport outputs actions as "0/1", this converts this to ['turnOff', 'turnOn']
def __get_actions_from_xml(homeport_actions):
    return map(mapper.map_id_to_action, homeport_actions.split('/'))