import SimpleHTTPServer
import SocketServer
import os
import json

port = int(os.environ.get("PORT", 5000))
rootdir = '/Server/'

class Device(object):
    def __init__(self, id, name, coords, actions):
        self.id = id
        self.name = name
        self.coords = coords
        self.actions = actions

device1 = Device(0, 'First Device', (0,1), ['turnOn', 'turnOff'])
device2 = Device(1, 'Second Device', (2,5), ['turnOn', 'turnOff'])
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
        elif self.path=='/devices/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            json_string = json.dumps([device.__dict__ for device in devices])
            self.wfile.write(json_string)
        else:
            self.send_error(404,'File Not Found: %s' % self.path)

customHandler = CustomHandler

httpd = SocketServer.TCPServer(("", port), customHandler)

print "serving at port", port
httpd.serve_forever()