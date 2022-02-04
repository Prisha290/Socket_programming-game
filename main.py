import socket
import sys
import threading
import hashlib


def server_program():
    # get hostname
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5050
    ThreadCount = 0
    # Socket instance
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind() takes tuple as an argument
    # binds the host address and port together
    try:
        server_socket.bind((HOST, PORT))
    except socket.error as e:
        print(str(e))
        sys.exit()

    print("[SERVER STARTED]")
    # Configure how many clients can listen simultaneously
    server_socket.listen(2)
    HashTable = {}

    while True:
        # Accept new connections
        conn, address = server_socket.accept()
        print("Connection from: ", str(address))

        client_handler = threading.Thread(target=threaded_client, args=(conn,))
        client_handler.start()
        ThreadCount += 1
        print("[THREAD #] ", str(ThreadCount))

    # while True:
    #   """
    #   Receive data stream.
    #   It won't accept data packet greater than 1024 bytes
    #   """
    #   data = conn.recv(1024).decode()
    #   if not data:
    #     # if data is not received we break
    #     break
    #   print("from connected user: ", str(data))
    #   data = input(' -> ')
    #   conn.send(data.encode())
    conn.close()


def threaded_client(connection):
    try:
        connection.send(str.encode("Welcome to the server!\n"))
        """
        Server Code for Welcome Menu. This will print on the client side:
        Press 1 to Login
        Press 2 to Register
        Type exit to disconnect
        """
        connection.send(str.encode("0"))
        # Request user input
        user_input = connection.recv(2048).decode()
        if user_input:
            print("User entered: ", user_input)

        # Check welcome menu input
        while check_user_input(user_input, 1, 2) == -1:
            connection.send(str.encode("Please enter a valid option: "))
            user_input = connection.recv(2048).decode()

        # try:
        #     connection.send(str.encode(f'[SERVER] You entered: {user_input}'))
        # except IOError as e:
        #     print("[IOError]", str(e))
        
        # Getting Username and Password for Login
        if user_input == '1':
            connection.send(str.encode("1"))
            username = connection.recv(2048).decode()
            password = connection.recv(2048).decode()
            print(f'[SERVER LOGIN] Username: {username} | Password: {password}')
        # Getting Username and Password for Register
        elif user_input == '2':
            connection.send(str.encode("2"))
            username = connection.recv(2048).decode()
            password = connection.recv(2048).decode()
            print(f'[SERVER REGISTER] Username: {username} | Password: {password}')
        # User is exiting, we close the connection
        else:
            connection.close()

    except ConnectionResetError as e:
        print("[USER FORCED DISCONNECT]")
        connection.close()




def check_user_input(data, start, end):
    if data == 'exit':
        # print("Bye")
        return 0
    if data.isnumeric():
        data = eval(data)
        if data >= start and data <= end:
            # print ("You entered: ", data)
            return 1
    return -1


if __name__ == '__main__':
    server_program()