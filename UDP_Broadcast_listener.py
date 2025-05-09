import socket
from IPy import IP

def listen():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)

    # create a socket object
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

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


listen()
