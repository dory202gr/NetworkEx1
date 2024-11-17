#!/usr/bin/env python3
import sys

from tcp_server import start_connection
from user_map import create_users_map
from apis import calculate_message

def test_calculation():
    assert calculate_message("calculate: 3+4") == "response: 7."
    assert calculate_message("calculate: 3-4") == "response: -1."
    assert calculate_message("calculate: 3*4") == "response: 12."
    assert calculate_message("calculate: 7/3") == "response: 2.33."
    assert calculate_message("calculate: 3^4") == "response: 81."
    assert calculate_message("calculate: 2147483647+1") == "error: result is too big"
    assert calculate_message("max: (3 4 5 6)") == "the maximum is 6"
    assert calculate_message("max: (-3 4 5 -6)") == "the maximum is 5"
    assert calculate_message("factor: 12") == "the prime factors of 12 are: 2,3"
    assert calculate_message("factor: 105") == "the prime factors of 105 are: 3,5,7"
    assert calculate_message("factor: 71") == "the prime factors of 71 are: 71"
    assert calculate_message("factor: 10251") == "the prime factors of 10251 are: 3,17,67"


def main():
    # test_calculation()
    port, users_file = arg_parser()
    users_map = create_users_map(users_file)

    start_connection(users_map, port)

def arg_parser():
    if len(sys.argv) < 2:
        print("Arguments missing")
        exit(1)
    users_file = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1337
    return port, users_file


if __name__ == "__main__":
    main()



