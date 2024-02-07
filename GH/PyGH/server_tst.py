import socket
import threading
import os
import json


def start_server():
    # Create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the port on which you want to connect
    port = 58260

    # Bind to the port
    server.bind(('127.0.0.1', port))

    # wait untill the first message is received than close the server
    server.listen(1)

    # Establish connection with client.
    client, addr = server.accept()
    print('Got connection from', addr)

    # Receive the data from the client
    data = client.recv(1024)
    print('Server received', data.decode())

    # Decode the data and convert it to a dictionary
    data = json.loads(data.decode())

    # Get the function name and the arguments
    msg = data['msg']

    print(f"Server received: {msg}")


# Start the server
start_server()