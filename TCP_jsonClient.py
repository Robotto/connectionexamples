#!/usr/bin/env python3
#KILDE: https://gist.github.com/ferstar/c112f6aeb9dd47727ac6
import socket
import json

#Server settings:
#default values:
#serverIP, serverPort = "10.147.162.44", 9527
serverIP, serverPort = "100.123.201.9", 9527

#Try to load server info from server_settings.json which is dumped by server when starting.
# Read JSON file
try:
    with open('server_settings.json') as data_file:
        data_loaded = json.load(data_file)
        serverIP = data_loaded['Addr']
        serverPort = int(data_loaded['PORT'])
        print(f'Loaded server settings from server_settings.json: {serverIP}:{serverPort}')
except FileNotFoundError:
    print('Server settings file not found. Falling back to hardcoded settings')

#Define some garbage data:
data = {
"name": "hello, I am Tom.",
"age": 10,
"info": "sample is simple."
}

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((serverIP, serverPort))
    print(f'Connected to {serverIP}:{serverPort}')
    outgoingPort=sock.getsockname()[1]
    print(f'My outgoing port is: {outgoingPort}')
    data['clientPort']=outgoingPort
    sock.send(bytes(json.dumps(data), 'UTF-8'))

    # Receive data from the server and shut down
    received = json.loads(sock.recv(1024).decode('UTF-8'))
finally:
    sock.close()

print ("Sent: {}".format(data))
print ("Received: {}".format(received))
