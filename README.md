# NetworkEx1 - TCP Calculator Server

## Overview

This project is a TCP-based client-server application that performs mathematical operations and prime factorization. The server authenticates users and provides calculation services after successful authentication. The client interacts with the server to send mathematical queries and receive responses.

## Features

- **Authentication**: Users must authenticate with a username and password.
- **Mathematical Operations**: The server supports the following operations:
  - Basic arithmetic: addition (+), subtraction (-), multiplication (*), division (/), and exponentiation (^).
  - Maximum value in a list: `max: (value1 value2 ...)`.
  - Prime factorization: `factors: number`.
- **Error Handling**:
  - Large results are flagged with an error message.
  - Invalid input patterns are handled gracefully.
- **Scalability**: Multiple clients can connect to the server simultaneously.

## Usage

### Running the Server

1. Prepare a user credentials file with each line containing a username and password (e.g., `users.txt`).
2. Run the server:
   ```bash
   python3 numbers_server.py users.txt <1337>
   
* Replace <port> with the desired port number (default is `1337`).

### Running the Client

1. Run the client:
   ```bash
   python3 numbers_client.py <server_hostname> <server_port>

* Replace `<server_hostname>` with the server's hostname or IP (default is `localhost`).
* Replace `<server_port>` with the server's port (default is `1337`).

2. Authenticate with a username and password.
3. After logging in, input mathematical queries or type `quit` to exit.

