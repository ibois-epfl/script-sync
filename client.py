#! python3

import socket

def send_file(server_address, server_port):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((server_address, server_port))

    # send the following path to the server
    path = "F:\ScriptSync\pyversion.py"
    client_socket.send(path.encode())

    # Close the socket
    client_socket.close()
    print(f"File path sent successfully.")

if __name__ == "__main__":
    server_address = '127.0.0.1'  # Change this to the server's IP address
    server_port = 12345  # Change this to the server's port number

    send_file(server_address, server_port)
