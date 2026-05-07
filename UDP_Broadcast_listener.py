import socket
from IPy import IP

#Asks user to select an IP, address as source for broadcasting.

def selectInterface():
    interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]

    print("Here's all the LAN IPs for this computer:")
    i=0
    for ip in allips:
        print(f"{i}: {ip}")
        i+=1
    choice = int(input("Which one would you like to use to transmit? "))
    interface = allips[choice]

    #interface = interface[0]
    #print(f"chose {interface}")
    # create a socket object

    return interface


def listen(IPAddr):
    #hostname = socket.gethostname()
    #IPAddr = socket.gethostbyname(hostname)

    #print("Your Computer IP Address is:" + IPAddr)

    # create a socket object
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #TX_port = 8001
    RX_port = 8002
    listen_addr = ("", RX_port)

    listener.bind(listen_addr)

    print(f"Listening on port {RX_port}")

    while True:
        data, addr = listener.recvfrom(1024)

        remoteIP = IP(addr[0]).strNormal()  # convert address of packet origin to string
        received = data.decode("utf-8")  # convert bytes to string

        print(f"Received {received} from {remoteIP}")

addr = selectInterface()
listen(addr)
