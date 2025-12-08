import socket
import threading
from des import encode
from rsa import encrypt, decrypt, generate_keypair,  sign_message, verify_sign


DES_KEY = "12345678"
BOB_PUBLIC_KEY, BOB_PRIVATE_KEY = generate_keypair(128)

ALICE_PUBLIC_KEY = None
        
def send_messages(conn):
    while True:
        msg = input("[bob] ")
        encrypted = encode(msg, DES_KEY, 'E')
        signed = sign_message(msg, BOB_PRIVATE_KEY)
        paket = f"{encrypted}.{signed}"
        conn.sendall(paket.encode())

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(4096).decode()
        chiper, sign = data.rsplit('.', 1)
        sign = int(sign)
        decrypted = encode(chiper, DES_KEY, 'D').rstrip('\x00')
        # decrypted += ' heker'
        valid = verify_sign(decrypted, sign, ALICE_PUBLIC_KEY)
        if valid:
            status = "VALID"
        else:
            status = "INVALID"
            
        # print(data.decode())
        print(f"\n[alice] {decrypted}   [{status}]\n[bob] ", end="", flush=True)

def main():
    host = input("Server IP: ")
    port = 5050

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))
    print("[bob] Connected to alice.")
    
    #terima pub key alice
    data = conn.recv(1024).decode()
    a_e, a_n = map(int, data.split(","))
    global ALICE_PUBLIC_KEY
    ALICE_PUBLIC_KEY = (a_e, a_n)
    print("[bob] Received Alice's public key:", ALICE_PUBLIC_KEY)
    
    #kirim pub key bob ke alice
    e, n = BOB_PUBLIC_KEY
    conn.sendall(f"{e},{n}".encode())
    print(f"[bob] Sent public key {BOB_PUBLIC_KEY} to alice.")
    
    #kirim des key ke alice dengan rsa
    des_int = int.from_bytes(DES_KEY.encode("ascii"), "big")
    encrypted_des = encrypt(des_int, ALICE_PUBLIC_KEY)
    print("[bob] DES key:", DES_KEY)
    print("[bob] Encrypted DES key:", encrypted_des)
    
    conn.sendall(str(encrypted_des).encode())
    print("[bob] Sent encrypted DES key to alice.")
    
    
    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()
    send_messages(conn)
    
if __name__ == "__main__":
    main()