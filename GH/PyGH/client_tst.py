import socket
import sys
import time

def start_client():
    # Create a socket object
    s = socket.socket()

    # Define the port on which you want to connect
    port = 58260

    # Connect to the server on local computer
    s.connect(('127.0.0.1', port))

    try:
        # Send a message to the server every 2 seconds
        while True:
            # Send a message to the server
            s.send("Hello server!".encode())

            # Wait for 2 seconds
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nCtrl-C - Stopping client")
        s.close()
        sys.exit(1)

# Start the client
start_client()