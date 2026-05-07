import socket

#Asks user to select an IP address to listen for broadcasted messages.

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



def getSocket(sourceIP):
    transmitter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    #print(broadcast_addr)
    transmitter.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    transmitter.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transmitter.bind((sourceIP, 0)) #open an outgoing port on chosen interface. Don't care about port number :)
    return transmitter

def transmit(msg, conn, dest):
        conn.sendto(tx,dest)


broadcast_Port = 8002
sourceIP = selectInterface()
broadcast_tuple = ('<broadcast>',broadcast_Port)
transmitter = getSocket(sourceIP)
print(f"Ready to TX from {sourceIP} to port {broadcast_Port}")

while True:
    tx = input("What to send?").strip().encode()  # convert string to bytes
    transmit(tx,transmitter,broadcast_tuple)
