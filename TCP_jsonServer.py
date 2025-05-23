#!/usr/bin/env python3
#KILDE: https://gist.github.com/ferstar/c112f6aeb9dd47727ac6
import socket
import socketserver, subprocess, sys
from ipaddress import IPv4Address
from threading import Thread
from pprint import pprint
import json


HOST = socket.gethostname()
Addr = socket.gethostbyname(HOST)
PORT = 9527

class SingleTCPHandler(socketserver.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    def handle(self):
        # self.request is the client connection
        data = self.request.recv(1024)  # clip input at 1Kb
        text = data.decode('utf-8')
        pprint(json.loads(text))
        for key in json.loads(text):
            pprint(json.loads(text)[key])
        self.request.send(bytes(json.dumps({"status":"success!"}), 'UTF-8'))
        self.request.close()

class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    print(f'Listening on {Addr} port {PORT}')
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)