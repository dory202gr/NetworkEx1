import sys
import socket

from consts import DEFAULT_CLIENT_PORT, DEFAULT_CLIENT_HOSTNAME


def main():
    cl_hostname, cl_port = cl_parse_args()
    pass

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
    cl_hostname = DEFAULT_CLIENT_HOSTNAME
    cl_port = DEFAULT_CLIENT_PORT
    return cl_hostname, cl_port


if __name__ == "__main__":
    main()