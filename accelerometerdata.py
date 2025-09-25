import socket
import pickle


ESP_IP: str = "10.147.162.42"  # replace with ESP32 IP from Serial Monitor
ESP_PORT: int = 8082

print(f"trying to load server info from accelerometerServer.pkl")
try:
    with open('accelerometerServer.pkl', 'rb') as file:
        # Load the pickled data
        data = pickle.load(file)
        ESP_IP = data['IP']
        ESP_PORT = data['PORT']
except FileNotFoundError:
    print(f"No server info found. Defaulting to: {ESP_IP}:{ESP_PORT}")

s: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ESP_IP, ESP_PORT))

while True:
    try:
        rx = s.recv(1024)
        ax,ay,az = rx.decode().split(",")
        print(f"AX:{float(ax)}, AY:{float(ay)}, AZ:{float(az)}")

    except:
        s.close()