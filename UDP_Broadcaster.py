import socket

def transmit():

    interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]


    # create a socket object
    transmitter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

    broadast_Port = 8002

    broadcast_addr = (socket.inet_aton('255.255.255.255'),broadast_Port)

    transmitter.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1023)

    transmitter.bind((allips[0], 0)) #open an outgoing port on first interface. Don't care about port number :)

    print(f"Read to TX on {broadcast_addr}")

    while True:

        tx = input("What to send?").strip().encode()  # convert bytes to string
        transmitter.sendto(tx,broadcast_addr)


transmit()
