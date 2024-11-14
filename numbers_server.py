#!/usr/bin/env python3
import sys
import socket
def main(users_file, port):
    # Load users from the specified file
    try:
        with open(users_file, 'r') as file:
            users_data = file.read()
            print(f"Loaded users data:\n{users_data}")
    except FileNotFoundError:
        print(f"Error: The file {users_file} was not found.")
        sys.exit(1)

    # Start a server socket to listen on the specified port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)
        print(f"Server started, listening on port {port}")

        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            with client_socket:
                # Receive data from the client
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Received data: {data}")

                # Send a simple response back to the client
                response = "Hello, you are connected to the numbers server!"
                client_socket.sendall(response.encode('utf-8'))
                print("Response sent to the client")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Arguments missing")
        sys.exit(1)

    users_file = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1337

    main(users_file, port)