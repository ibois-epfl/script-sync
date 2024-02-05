import socket
import threading
import os
import json

def handle_client(client_socket):
    try:
        while True:
            # Receive data from the client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            # obj = json.loads(message)
            print(f"{message}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection with the client
        client_socket.close()

def start_server():
    # Create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the port on which you want to connect
    port = 58260

    # Bind to the port
    server.bind(('127.0.0.1', port))

    # Put the socket into listening mode
    server.listen(5)
    print('Server is listening')

    # Set a timeout for the accept() method
    server.settimeout(1)

    try:
        while True:
            try:
                # Accept a new client connection
                client_socket, addr = server.accept()
                # print(f"Accepted connection from: {addr[0]}:{addr[1]}")
                # data_str = client_socket.recv(1024).decode('utf-8')
                # print(f"Received data string: {data_str}")

                # # if the data_str is empty, continue to the next iteration
                # if not data_str or data_str == "":
                #     continue

                # try:
                #     obj = json.loads(data_str)
                #     print(f"Received data: {obj}")
                # except Exception as e:
                #     print(f"An error occurred: {e}")




                # Start a new thread to handle this client connection
                client_handler = threading.Thread(target=handle_client, args=(client_socket,))
                client_handler.start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\nServer is stopping due to keyboard interruption...")
        server.close()
        os._exit(1)

# Start the server
start_server()