import socket
import select

from apis import verify_pattern, calculate_message


def start_connection(users_map, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('', port))
        server_socket.listen(5)
        sockets_list = [server_socket]
        clients_authenticates_and_message = {}
        server_socket.setblocking(False)
        print(f"Server started, listening on port {port}")

        while True:
            readable, writable, _ = select.select(sockets_list, sockets_list, [], 5)

            for readable_soc in readable:
                if readable_soc == server_socket:
                    try:
                        client_socket, client_address = server_socket.accept()
                        print(f"Connection from {client_address}")
                        client_socket.setblocking(False)
                        sockets_list.append(client_socket)
                        clients_authenticates_and_message[client_socket] = {"isAuth": False, "res": "Welcome! Please log in."}
                    except BlockingIOError:
                        print("No connection to accept.")
                else:
                    try:
                        message = readable_soc.recv(1024)
                        if not message:
                            disconnect_client(readable_soc, sockets_list, clients_authenticates_and_message)
                            continue
                        else:
                            if not clients_authenticates_and_message[readable_soc]["isAuth"]:  # not authenticated
                                is_auth, username = authenticate(readable_soc,users_map, message)
                                if is_auth:
                                    clients_authenticates_and_message[readable_soc] = {"isAuth": True, "res": f"Hi {username}, good to see you."}
                                    writable.remove(readable_soc)
                                else:
                                    if not username:
                                        disconnect_client(readable_soc, sockets_list, clients_authenticates_and_message) # disconnect client socket
                                    else:
                                        clients_authenticates_and_message[readable_soc] = {"isAuth": False, "res": "Failed to login."}
                                        writable.remove(readable_soc)
                                continue
                            response = calculate_message(message)
                            if not response:
                                disconnect_client(readable_soc, sockets_list, clients_authenticates_and_message)
                                continue
                            if response == "quit":
                                disconnect_client(readable_soc, sockets_list, clients_authenticates_and_message)
                            clients_authenticates_and_message[readable_soc] = {"isAuth": True, "res": response}
                            writable.remove(readable_soc)
                    except Exception as e:
                        disconnect_client(readable_soc, sockets_list, clients_authenticates_and_message)
                        continue

            for writable_soc in writable:
                if writable_soc != server_socket:
                    total_send = sendall(writable_soc, clients_authenticates_and_message[writable_soc]["res"].encode())
                    print(f"# of bytes sent: {total_send}")


def disconnect_client(soc, sockets_list, clients_authenticates_and_message):
    sockets_list.remove(soc)
    del clients_authenticates_and_message[soc]
    sendall(soc, "you've been disconnected from the server")
    soc.close()


def sendall(client_socket, message):
    total_send = 0

    while total_send < len(message):
        count_sent = client_socket.send(message[total_send:])
        if count_sent == 0:
            break
        total_send += count_sent

    return total_send


def authenticate(client_soc, users_map, message):
    decoded_auth = message.decode()
    if verify_pattern(decoded_auth, r"User: (\S+)\nPassword: (\S+)"):
        return False, None
    credentials = decoded_auth.split("\n")
    username = credentials[0].split(": ")[1]
    password = credentials[1].split(": ")[1]
    if username not in users_map:
        return False, ""
    return users_map[username] == password, username

