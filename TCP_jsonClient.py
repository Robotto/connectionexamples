#!/usr/bin/env python3
#KILDE: https://gist.github.com/ferstar/c112f6aeb9dd47727ac6
import socket
import json

HOST, PORT = "localhost", 9527
data = {
"name": "hello, I am Tom.",
"age": 10,
"info": "sample is simple."
}

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.send(bytes(json.dumps(data), 'UTF-8'))

    # Receive data from the server and shut down
    received = json.loads(sock.recv(1024).decode('UTF-8'))
finally:
    sock.close()

print ("Sent: {}".format(data))
print ("Received: {}".format(received))