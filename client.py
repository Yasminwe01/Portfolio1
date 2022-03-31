import socket
import sys
import os
import threading
from Bots import *  # Import all bot functions from Bot.py.

ip = sys.argv[1]
port = int(sys.argv[2])
bot = sys.argv[3]
# All the bots that can you select from:
bots = {"batman": batman,
        "joker": joker,
        "superman": superman, "spiderman": spiderman}

#Instantiate client socket:
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Attempt to connect to server
client_socket.connect((ip, port))
client_socket.setblocking(False)
# Sends the bot'name you selected to the server
client_socket.send((bot.capitalize()).encode())
print(f"You have selected Bot: {bot.capitalize()}, and are now connected to server at {ip}:{port}...")
print("Waiting for suggestion from server...")


# Function that returns the actions
def receive_message(server=None,
                    client=None):
    msg = client_socket.recv(1024)
    if not len(msg):  # if the message is an empty string, assume server is disconnecting
        print('Connection closed by server')
        os._exit(0)
    # This if statment checks the host's message
    if msg.decode().find("Host") != -1:
        print(f"\n---------------CHATROOM-------------")
        print(f"{msg.decode()}")
        server = [action for action in actions if msg.decode().find(action) != -1][0]
        return (server, client)
    else:
        client = [action for action in actions if msg.decode().find(action) != -1][
            0]  # Loop over all actions and check if that action can be found in the message
        return (server, client)


# Send a message to the server
def send_msg(server, client):
    msg = (f"{bot.capitalize()}: " + bots[bot](server, client)).encode()
    print(f"{msg.decode()}\n")
    client_socket.send(msg)


def input_thread():
    while True:
        inpt = input()
        if inpt == 'q' or inpt == 'quit':
            client_socket.close()
            os._exit(0)


threading.Thread(target=input_thread).start()
# loop that bot sends messages and receive

server_action, client_action = "", None
while True:
    if server_action:
        send_msg(server_action, client_action)
    server_action, client_action = "", None

    try:
        server_action, client_action = receive_message()
    except Exception as e:
        if e is SystemExit:
            break
