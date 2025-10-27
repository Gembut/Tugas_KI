import socket
import threading
from des import encode

KEY = "12345678"  # key 8 karakter

def send_messages(conn):
    while True:
        msg = input("Server: ")
        encrypted = encode(msg, KEY, 'E')
        conn.sendall(encrypted.encode())

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(4096)
        decrypted = encode(data.decode(), KEY, 'D')
        print(f"\nClient: {decrypted}\nServer: ", end="", flush=True)
    
def main():
    host = "0.0.0.0"  # bind semua interface
    port = 5050

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on port {port}...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()
    send_messages(conn)

if __name__ == "__main__":
    main()
