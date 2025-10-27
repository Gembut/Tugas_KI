import socket
import threading
from des import encode  

KEY = "12345678"  # key 8 karakter

def send_messages(conn):
    while True:
        msg = input("Client: ")
        encrypted = encode(msg, KEY, 'E')
        conn.sendall(encrypted.encode())

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(4096)
        decrypted = encode(data.decode(), KEY, 'D')
        print(f"\nServer: {decrypted}\nClient: ", end="", flush=True)

def main():
    host = input("IP server: ")
    port = 5050

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server!")

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    send_messages(client_socket)

if __name__ == "__main__":
    main()
