import socket 
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #Your WLAN IP address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# AF_INET refers to the address-family ipv4.
# SOCK_STREAM means connection-oriented TCP protocol.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind(): binds it to a specific IP and port so that it can listen to incoming requests on that IP and port.
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()
        

def start():
    # listen(): puts the server into listening mode
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # accept(): The accept method initiates a connection with the client
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()