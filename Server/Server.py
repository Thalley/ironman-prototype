import SimpleHTTPServer
import SocketServer
import os

port = int(os.environ.get("PORT", 5000))
rootdir = '/Server/'
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

customHandler = CustomHandler

httpd = SocketServer.TCPServer(("", port), customHandler)

print "serving at port", port
httpd.serve_forever()