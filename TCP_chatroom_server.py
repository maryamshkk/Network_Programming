# Chat room connection - Client-To-Client
import threading
import socket

host = '127.0.0.1'
port = 56789
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []

# send message to all clients at once
def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room'.encode('utf-8'))
            aliases.remove(alias)
            break

def info_recieve():
    while True:
        print("Server is running and listening")
        client, address = server.accept()
        print(f'Connection has been established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        # add clients and aliases to list
        clients.append(client)
        aliases.append(alias)

        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to TCP Chat Room'.encode('utf-8'))
        client.send('You are now connected'.encode('utf-8'))

    #specific connection with specific client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()  

if __name__ == "__main__":
    info_recieve()
    
