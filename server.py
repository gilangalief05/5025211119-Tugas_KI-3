import threading
import socket
import DES

host = "127.0.0.1" # or localhost
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
users = []

def broadcast (message):
    print(message)
    for client in clients:
        client.send(message.encode("utf-8"))

def handle (client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = users[index]
            broadcast(f"{username} left the chat")
            users.remove(username)
            if not users:
                server.close()
            break

def receive():
    while True:
        client, address = server.accept()
        if len(clients) >= 2:
            client.close()
            continue
        else:
            print(f"Connected with {str(address)}")

            client.send("name".encode("utf-8"))
            username = client.recv(1024).decode("utf-8")
            users.append(username)
            clients.append(client)

            print(f"Username of the client is {username}")
            broadcast(f"{username} joined the chat")
            client.send("Connected to the server".encode("utf-8"))

            thread = threading.Thread(target=handle, args=(client, ))
            thread.start()


print("Server is listening...")
receive()