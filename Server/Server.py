import SimpleHTTPServer
import SocketServer
import os
import cgi
import json
from bs4 import BeautifulSoup

port = int(os.environ.get("PORT", 5000))
rootdir = '/Server/'

class Device(object):    
    def __init__(self, id, name, coords, actions, state = 'off'):
        self.id = id
        self.name = name
        self.coords = coords
        self.actions = actions
        self.state = state

    def canPerformAction(self, action):
      return action in self.actions

    def performAction(self, action):
      if action == 'turnOn':
        self.state = 'on'
      elif action == 'turnOff':
        self.state = 'off'

device1 = Device(0, 'Lamp at Couches', (6.50, 3.35), ['turnOn', 'turnOff'])
device2 = Device(1, 'Lamp at Dinner Table', (2.68, 1.92), ['turnOn', 'turnOff'])
devices = [device1, device2]

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):

        if self.path=='/':
            f = open(os.curdir + os.sep + rootdir + 'index.html')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        elif self.path=='/devices/' or self.path=='/devices':
            self.send_response(200)
            self.send_header('Content-type', 'application/json') 
            self.end_headers()

            json_string = json.dumps([device.__dict__ for device in devices])
            self.wfile.write(json_string)
        else:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        action = postvars.get('action', "NA")[0]
        ident = postvars.get('id', "NA")[0]

        if action=="N" or ident=="N":
            self.send_response(400)
            return None

        matching_devices = [ d for d in devices if d.id == int(ident) ]
        device = matching_devices[0] if len(matching_devices) > 0 else None
        if device == None or not device.canPerformAction(action):
          self.send_response(400)
          return None

        device.performAction(action)
        
        color = 'green' if device.state == 'on' else 'red'
        soup = BeautifulSoup(open(os.curdir + os.sep + rootdir + 'index.html'), "html.parser")
        soup.find(id=ident)['style'] = "background-color: " + color
        with open(os.curdir + os.sep + rootdir + 'index.html', "wb") as file:
            file.write(str(soup))
        self.send_response(200)

customHandler = CustomHandler

httpd = SocketServer.TCPServer(("", port), customHandler)

print "serving at port", port
httpd.serve_forever()
