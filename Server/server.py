# Runs the server containing the location info of
# devices and handles calls to the smart hub
from flask import Flask, jsonify, request
from device import Device
import json
 
#Server code begins
app = Flask(__name__)

#Performs an action on a device
@app.route('/', methods=['POST'])
def do_action():
    action = request.form['action']
    id = request.form['id']
    print(action)
    print(id)
    return "Action " + action + " performed on device with ID " + id

#Gets the list of devices
@app.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(devices=[d.serialize() for d in devices])

#Starts the server
if __name__ == '__main__':
    app.debug = True
    app.run()