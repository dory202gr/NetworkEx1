import sys
import socket

from consts import DEFAULT_SERVER_PORT, DEFAULT_SERVER_HOSTNAME


def main():
    sr_hostname, sr_port = cl_parse_args()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    authenticate(server_socket, sr_hostname, sr_port)
    pass


def authenticate(server_socket, sr_hostname, sr_port):
    server_socket.connect((sr_hostname, sr_port))
    print(server_socket.recv(1024))


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