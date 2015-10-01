import SimpleHTTPServer
import SocketServer

port = int(os.environ.get("PORT", 5000))

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", port), Handler)

print "serving at port", port
httpd.serve_forever()