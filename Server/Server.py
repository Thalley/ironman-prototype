import SimpleHTTPServer
import SocketServer
import os
import cgi

port = int(os.environ.get("PORT", 5000))
rootdir = '/Server/'


devices=['dev1', 'dev2', 'dev3']

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

            self.wfile.write("<html><head><title>Title goes here.</title></head>")
            self.wfile.write("<body><p>This is a test.</p>")
            self.wfile.write("<p>You accessed path: %s</p>" % self.path)
            self.wfile.write("</body></html>")
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
        if action=="NA" or ident=="NA":
            return None
        self.wfile.write(ident + " did action " + action) # replace with whatever action to do



customHandler = CustomHandler

httpd = SocketServer.TCPServer(("", port), customHandler)

print "serving at port", port
httpd.serve_forever()