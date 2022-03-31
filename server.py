import select
import socket
import sys
import threading
from Bots import *

try:
    port = int(sys.argv[2])
    host = ""
    if port == '--help' or port == '-h':
        print("")
        sys.exit()
except (IndexError, ValueError):
    print('-------------------------------')
    print("To start a server you have to connect to specified ip and port:\n")
    sys.exit()

print(f'Listening for connections on {host}:{port}...')

# Bind the server to ip and port and listen for clients
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
# listen is used below to mark our socket instance as a passive socket
# - A socket that will be used to accept inncoming requess with the accept() method
server_socket.listen(4)
FORMAT = 'utf-8'
socket_list = [server_socket]
clients = {}  # Lists for clients
names = []
msg_count = 0
expected_msg_count = 0


def receive():  # A function that adds clients to the socket list
     # our server is now listening for connections.
    # When a client attempts to connect, we use the accept()
    # mehod to establish a connection
    conn, address = server_socket.accept()
    socket_list.append(conn)
    name = conn.recv(2042).decode()
    names.append(name)  # Add client to names array to wait until next round of conversations
    print(str.upper('\n'f'{name} has joined the chatroom\n'))
    # sends a message from our server socket to client socket
    conn.send('Connected to the server'.encode(FORMAT))


def handle_client(list):
    global msg_count, expected_msg_count
    try:  # try and except to check if the client is still connected
        msg = list.recv(2042)
    except ConnectionAbortedError:
        print(f"{clients[list]} disconnected.")
        socket_list.remove(list)
        del clients[list]

    print(f"{msg.decode()}")
    msg_count += 1
    # Broadcast to all clients
    for client in clients:
        if client == list:
            continue
        client.send(msg)


def send_suggestion():
    global msg_count, expected_msg_count
    print('\n'
          "You have thesse options to choose from:"'\n'
          '\n'"1: lets go outside and play"
          '\n'"2: Let's take a walk to Iron man"
          '\n'"3: Let's sleep a little bit!,"
          '\n'"4: I feel like fighting right now ,"
          '\n'"5: We can do some eating")
    inpt = input('\n'
                 f"Select a suggestion by index (1-{len(suggestions)}): ")  # Let user choose which suggestion to pick
    print(f"\n---------------CHATROOM-------------")
    suggestion = "Host: " + suggestions[
        int(inpt) - 1]
    for client in clients:
        try:
            client.send(suggestion.encode())
            expected_msg_count += 1
        except:
            socket_list.remove(client)
    return True


# Created a while loop to loop between server and client.
# Which runs untill we stop out server program
while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], socket_list)
    for list in read_sockets:
        if list != server_socket:
            handle_client(list)
        else:
            receive()
    for list in error_sockets:
        socket_list.remove()

    if msg_count == expected_msg_count:
        for index, name in enumerate(names):
            clients[socket_list[-len(names) + index]] = name
        print('-------------------------------')

        msg_count = 0
        expected_msg_count = 0
        if not send_suggestion(): break
