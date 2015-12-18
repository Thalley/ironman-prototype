# Runs the server containing the location info of
# devices and handles calls to the smart hub
from flask import Flask, jsonify, request, abort
from device import Device
import json
import homeport_adapter
# from logger import log

#Server code begins
app = Flask(__name__)

DEVICES = []
for count in xrange(5):
    DEVICES.append(Device(str(count), "dev" + str(count), (count,1), ['turnOn', 'turnOff'], 'URL'))

#Performs an action on a device
@app.route('/', methods=['POST'])
def do_action():
    action = request.form['action']
    id = request.form['id']
    #If we don't get an ID and an action
    if(not (id and action)):
        abort(400)

    #Find device by ID
    devices = DEVICES #homeport_adapter.request_homeport_devices()
    deviceByID = next((dev for dev in devices if str(dev.id) == id), None)

    #No device found
    if(not deviceByID):
        abort(404)

    #Device could not perform action
    if(not deviceByID.canPerformAction(action)):
        abort(400)    

    return "Done"
    # responsecode = homeport_adapter.do_homeport_action(deviceByID, action)
    # #Perform action
    # if(responsecode == 200):
    # 	return "Action \"" + action + "\" performed on device \"" + deviceByID.name + "\"" 
    # else:
    # 	abort(responsecode)

#Gets the list of devices
@app.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(devices=[d.serialize() for d in DEVICES])

#Starts the server
if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=False)