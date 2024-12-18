#!/usr/bin/env python3
import sys
import socket

from consts import DEFAULT_SERVER_PORT, DEFAULT_SERVER_HOSTNAME, FAILED_TO_LOGIN


def main():
    sr_hostname, sr_port = cl_parse_args()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    authenticate(client_socket, sr_hostname, sr_port)
    while True:
        operation = input()
        client_socket.send(operation.encode())
        data = client_socket.recv(1024)
        decoded_data = data.decode()
        print(decoded_data)
        if decoded_data == "you've been disconnected from the server":
            break
    client_socket.close()




def authenticate(server_socket, sr_hostname, sr_port):
    server_socket.connect((sr_hostname, sr_port))

    # print "Welcome! Please log in."
    print(server_socket.recv(1024).decode())

    while True:
        user_name = input("User: ")
        password = input("Password: ")
        server_socket.send(f"User: {user_name}\nPassword: {password}".encode())
        response = server_socket.recv(1024).decode()
        print(response)
        if response != FAILED_TO_LOGIN:
            break


def cl_parse_args():
    if len(sys.argv) > 3:
        print("Too many arguments")
        exit(1)

    cl_hostname, cl_port = default_arg_values()

    if len(sys.argv) == 3:
        cl_port = sys.argv[2]
    if len(sys.argv) == 2:
        cl_hostname = sys.argv[1]

    return cl_hostname, cl_port


def default_arg_values():
    sr_hostname = DEFAULT_SERVER_HOSTNAME
    sr_port = DEFAULT_SERVER_PORT
    return sr_hostname, sr_port


if __name__ == "__main__":
    main()