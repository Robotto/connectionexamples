import socket
import random
import time
import pickle

#KILDE https://www.datacamp.com/tutorial/a-complete-guide-to-socket-programming-in-python

def run_server():
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 8080

    hostname = socket.gethostname()
    server_ip = socket.gethostbyname(hostname)

    # bind the socket to a specific address and port
    server.bind((server_ip, port))
    # listen for incoming connections
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")

    ## pickle server info, så client kan loade det:
    serverData={"IP":server_ip, "PORT":port}
    with open('accelerometerServer.pkl', 'wb') as file:
        pickle.dump(serverData, file, protocol=pickle.HIGHEST_PROTOCOL)

    # accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # receive data from the client
    while True:
        try:
            ax = random.random()
            ay = random.random()
            az = random.random()


            txStr = f"{ax},{ay},{az}\n"
            print("TX:",txStr[0:-1])
            client_socket.send(txStr.encode())

            time.sleep(0.1)

        except:
            client_socket.close()
            print("Connection to client closed")
            # close server socket
            server.close()
            return

while True:
    run_server()
