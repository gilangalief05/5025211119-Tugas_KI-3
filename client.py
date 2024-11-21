import socket
import threading
import DES
import RSA

username = input("Input your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 5555

name_recv = ""
DES_key = ""
DES_pk_self = []
public_key_self = None
private_key_self = None
n_self = None
public_key_recv = None
n_recv = None

def receive():
    global DES_key, DES_pk_self, public_key_self, public_key_recv, private_key_self, n_recv, n_self, name_recv
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "name":
                client.send(username.encode("utf-8"))
            else:
                if message == "":
                    client.close()
                    break
                if ":" not in message:
                    print(message)
                    if "left the chat" in message:
                        public_key_recv = None
                        n_recv = None
                    elif "Connected" not in message and "joined" not in message:
                        if public_key_recv == None and n_recv == None and username not in message:
                            command = []
                            command = message.split(' ')
                            public_key_recv = int(command[1])
                            n_recv = int(command[2])
                            print(f"Receiver's public key: {public_key_recv}")
                            print(f"Receiver's n: {n_recv}")
                            client.send(f"[{username}] {str(public_key_self)} {str(n_self)} {' '.join(str(x) for x in DES_pk_self)}".encode("utf-8"))
                        if public_key_recv != None and n_recv != None and username not in message:
                            DES_pk_recv = message.split()
                            DES_pk_recv = DES_pk_recv[3:]
                            print("Result:", [int(i) for i in DES_pk_recv])
                            DES_enc = RSA.decoder([int(i) for i in DES_pk_recv], public_key_self, n_self)
                            print("Result:", DES_enc)
                            DES_pr_self = RSA.encoder(DES_enc, private_key_self, n_self)
                            print("Result:", DES_pr_self)
                            DES_recv = RSA.decoder(DES_pr_self, public_key_recv, n_recv)
                            print("Result:", DES_recv)
                else:
                    name_recv, message_enc = message.split(": ")
                    message_dec = DES.decrypt_str(message_enc, DES_key)
                    print(f"{name_recv}: {message_dec}")
                    # print(message)
        except:
            print("[Receive] An error occured!")
            client.close()
            break

def write():
    global DES_key, DES_pk_self, public_key_self, private_key_self, public_key_recv, n_self
    DES_key = DES.call_key()
    key = RSA.call_key()
    private_key_self = key[0]
    public_key_self = key[1]
    n_self = key[2]
    DES_pk_self = RSA.encoder(DES_key, private_key_self, n_self)
    print(f"DES key: {DES_key}\npublic key: {public_key_self}\nprivate key: {private_key_self}\nn: {n_self}")
    client.send(f"[{username}] {str(public_key_self)} {str(n_self)} {' '.join(str(x) for x in DES_pk_self)}".encode("utf-8"))
    while True:
        try:
            message = f"{username}: {DES.encrypt_str(input(""), DES_key)}"
            client.send(message.encode("utf-8"))
            # client.send(message.encode("utf-8"))
        except:
            print("[WRITE] An error occured!")
            client.close()
            break

try:
    client.connect((host, port))
except:
    client.close()
else:
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()