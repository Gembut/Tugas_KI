import socket
import threading
from des import encode
from rsa import generate_keypair, decrypt, encrypt, sign_message, verify_sign

DES_KEY = None
ALICE_PUBLIC_KEY, ALICE_PRIVATE_KEY = generate_keypair(128)

BOB_PUBLIC_KEY = None

def send_messages(conn):
    while True:
        msg = input("[alice] ")
        encrypted = encode(msg, DES_KEY, 'E')
        signed = sign_message(msg, ALICE_PRIVATE_KEY)
        paket = f"{encrypted}.{signed}"
        conn.sendall(paket.encode())

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(4096).decode()
        chiper, sign = data.rsplit('.', 1)
        sign = int(sign)
        decrypted = encode(chiper, DES_KEY, 'D').rstrip('\x00') 
        # decrypted += ' heker'
        valid = verify_sign(decrypted, sign, BOB_PUBLIC_KEY)
        if valid:
            status = "VALID"
        else:
            status = "INVALID"
            
        # print(data.decode())
        print(f"\n[bob] {decrypted}   [{status}]\n[alice] ", end="", flush=True)

def main():
    host = "0.0.0.0"
    port = 5050

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("[alice] Listening on port", port)

    conn, addr = server_socket.accept()
    print("[alice] Connected by", addr)
    
    #kirim pub key alice ke bob
    e, n = ALICE_PUBLIC_KEY
    conn.sendall(f"{e},{n}".encode())
    print(f"[alice] Sent public key {ALICE_PUBLIC_KEY} to bob.")
    
    #terima pub key bob
    data = conn.recv(1024).decode()
    b_e, b_n = map(int, data.split(","))
    global BOB_PUBLIC_KEY
    BOB_PUBLIC_KEY = (b_e, b_n)
    print("[alice] Received Bob's public key:", BOB_PUBLIC_KEY)
    
    #terima des key dari bob
    encrypted_des = int(conn.recv(1024).decode())
    print("[alice] Received encrypted DES key:", encrypted_des)

    #decrypt des key dengan rsa
    global DES_KEY
    decrypted_des = decrypt(encrypted_des, ALICE_PRIVATE_KEY)
    DES_KEY = decrypted_des.to_bytes(8, "big").decode("ascii")
    print("[alice] Decrypted DES key:", DES_KEY)

    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()
    send_messages(conn)




if __name__ == "__main__":
    main()