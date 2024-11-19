import socket
import select
from enum import Enum

from apis import verify_pattern, calculate_message
from consts import FAILED_TO_LOGIN


class TCPServer:

    class AuthStatus(Enum):
        SUCCESS = 0
        FAILED = 1
        WRONG_PATTERN = 2

    class SocketMessage:
        def __init__(self, sock, message):
            self.sock = sock
            self.message = message

    def __init__(self, users_map, port):
        self.sockets = []
        self.not_authenticates = []
        self.pending_authentication = []
        self.authenticated = []
        self.pending_response = []
        self.disconnect_socket = []
        self.users_map = users_map
        self.port = port


    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self._start_server(server_socket)

            while True:
                readable, writable, _ = select.select(self.sockets, self.sockets, [], 0)

                if server_socket in readable:
                    try:
                        self._accept_new_socket(server_socket)
                    except BlockingIOError:
                        print("No connection to accept.")

                self._process_not_authenticated_sockets(readable)

                self._process_authenticated_sockets(readable)

                self._process_disconnected_sockets(writable)

                self._process_pending_auth_sockets(writable)

                self._process_pending_response_sockets(writable)

    def _process_authenticated_sockets(self, readable):
        sockets_to_remove = []
        for authenticated_socket in self.authenticated:
            if authenticated_socket not in readable:
                continue

            self._process_authenticated_socket(authenticated_socket)
            sockets_to_remove.append(authenticated_socket)

        for socket_to_remove in sockets_to_remove:
            self.authenticated.remove(socket_to_remove)

    def _process_authenticated_socket(self, authenticated_socket):

        message = authenticated_socket.recv(1024)
        response = calculate_message(message.decode())

        if not response or response == "quit":
            self.disconnect_socket.append(authenticated_socket)
        else:
            self.pending_response.append(TCPServer.SocketMessage(authenticated_socket,
                                                                message=response))

    def _process_not_authenticated_sockets(self, readable):

        sockets_to_remove = []
        for not_authenticated_socket in self.not_authenticates:
            if not_authenticated_socket not in readable:
                continue

            self._process_not_authenticated_socket(not_authenticated_socket)
            sockets_to_remove.append(not_authenticated_socket)

        for socket_to_remove in sockets_to_remove:
            self.not_authenticates.remove(socket_to_remove)

    def _process_not_authenticated_socket(self, not_authenticated_socket):

        message = not_authenticated_socket.recv(1024)
        auth_status, username = self._authenticate(message)
        if auth_status == TCPServer.AuthStatus.WRONG_PATTERN:
            self.disconnect_socket.append(not_authenticated_socket)
        elif auth_status == TCPServer.AuthStatus.FAILED:
            self.pending_authentication.append(
                TCPServer.SocketMessage(not_authenticated_socket, message=FAILED_TO_LOGIN))
        else:
            self.pending_response.append(
                TCPServer.SocketMessage(not_authenticated_socket,
                                        message=f"Hi {username}, good to see you. "))

    def _process_disconnected_sockets(self, writable):
        sockets_to_remove = []
        for disconnect_socket in self.disconnect_socket:
            if disconnect_socket not in writable:
                continue
            self._process_disconnect_sockets(disconnect_socket)
            sockets_to_remove.append(disconnect_socket)

        for socket_to_remove in sockets_to_remove:
            self.disconnect_socket.remove(socket_to_remove)

    def _process_disconnect_sockets(self, disconnect_socket):
        self._sendall(disconnect_socket, b"you've been disconnected from the server")
        disconnect_socket.close()
        self.sockets.remove(disconnect_socket)

    def _process_pending_auth_sockets(self, writable):
        sockets_to_remove = []
        for pending_auth_socket_message in self.pending_authentication:
            if pending_auth_socket_message.sock not in writable:
                continue
            self._process_pending_auth_socket(pending_auth_socket_message)
            sockets_to_remove.append(pending_auth_socket_message)

        for socket_to_remove in sockets_to_remove:
            self.pending_authentication.remove(socket_to_remove)

    def _process_pending_auth_socket(self, pending_auth_socket_message):
        message_to_send = pending_auth_socket_message.message
        if message_to_send == "Failed to login." or message_to_send == "Welcome! Please log in.":
            self.not_authenticates.append(pending_auth_socket_message.sock)
        else:
            self.authenticated.append(pending_auth_socket_message.sock)
        self._sendall(pending_auth_socket_message.sock, message_to_send.encode())

    def _process_pending_response_sockets(self, writable):
        sockets_to_remove = []
        for pending_response_socket_message in self.pending_response:
            if pending_response_socket_message.sock not in writable:
                continue
            self._process_pending_response_socket(pending_response_socket_message)
            sockets_to_remove.append(pending_response_socket_message)

        for socket_to_remove in sockets_to_remove:
            self.pending_response.remove(socket_to_remove)

    def _process_pending_response_socket(self, pending_response_socket_message):
        message_to_send = pending_response_socket_message.message
        self.authenticated.append(pending_response_socket_message.sock)
        self._sendall(pending_response_socket_message.sock, message_to_send.encode())

    def _accept_new_socket(self, server_socket):
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        client_socket.setblocking(False)
        self.sockets.append(client_socket)
        self.pending_authentication.append(TCPServer.SocketMessage(client_socket, message="Welcome! Please log in."))

    def _start_server(self, server_socket):
        server_socket.bind(('', self.port))
        server_socket.listen(5)
        self.sockets.append(server_socket)
        server_socket.setblocking(False)
        print(f"Server started, listening on port {self.port}")

    def _sendall(self, client_socket, message):
        total_send = 0

        while total_send < len(message):
            count_sent = client_socket.send(message[total_send:])
            if count_sent == 0:
                break
            total_send += count_sent

        return total_send

    def _authenticate(self, message):
        decoded_message = message.decode()
        if not verify_pattern(decoded_message, r"User: (\S+)\nPassword: (\S+)"):
            return TCPServer.AuthStatus.WRONG_PATTERN, None
        credentials = decoded_message.split("\n")
        username = credentials[0].split(": ")[1]
        password = credentials[1].split(": ")[1]
        if username not in self.users_map:
            return TCPServer.AuthStatus.FAILED, ""
        return (TCPServer.AuthStatus.SUCCESS if self.users_map[username] == password else TCPServer.AuthStatus.FAILED,
                username)

