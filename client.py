import socket
import getpass # for password input
import auth
import time
# from dotenv import load_dotenv

# env_host = config('HOST')
# env_port = config('PORT')
# print(env_host, env_port)

def client_program(HOST, PORT):
    try:
        # Data packet size is 2048 bytes to be received from server
        SIZE = 2048

        # Socket instance
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        client_socket.connect((HOST, PORT))

        # Receive Welcome message
        response = client_socket.recv(SIZE).decode()
        print(response)
        # Receive Welcome Menu code from server
        response = client_socket.recv(SIZE).decode()
        # Print Welcome Menu
        menu_code(response, client_socket)
        
        # Receive next menu code from server
        while response:
            response = client_socket.recv(SIZE).decode()
            # print(response)
            menu_code(response, client_socket)
    except OSError as e:
        print('Goodbye!')

def menu_code(code, client_socket):
    if code == "0":
        print("Press 1 to Login")
        print("Press 2 to Register")
        print("Type exit to disconnect")
        user_input = input(' -> ')
        if user_input == "exit":
            # Send exit code to server
            client_socket.send(str.encode(user_input))
            # Close client connection
            client_socket.close()
            return
        client_socket.send(str.encode(user_input))
    elif code == "1":
        print("\nLogin dialog")
        
        username = input("Username: ")
        while auth.check_username(username) == False:
            print("Username must be at least 3 characters long and only letters")
            username = input("Username: ")
            username = username.lower()
        client_socket.send(str.encode(username))
        
        # Password input
        password = getpass.getpass()
        while auth.check_password(password) == False:
            print("Password must be at least 4 characters long.")
            password = getpass.getpass()
        print("Sending password to server...")
        # Hash the password entered by the user
        # password = auth.hash_password(password)
        client_socket.send(str.encode(password))

    elif code == "2":
        print("\nRegistration dialog")

        username = input("Username: ")
        while auth.check_username(username) == False:
            print("Username must be at least 3 characters long and only letters")
            username = input("Username: ")
            username = username.lower()
        client_socket.send(str.encode(username))

        # Password input
        password = getpass.getpass()
        while auth.check_password(password) == False:
            print("Password must be at least 4 characters long.")
            password = getpass.getpass()

        # Hash the password entered by the user
        password = auth.hash_password(password)
        client_socket.send(str.encode(password))

    elif code == "3":
        print("\nWelcome to Maze Runner")
        print("Press 1 to see highscores")
        print("Press 2 to see game rules")
        print("Press 3 to play/view a game")
        print("Type exit to disconnect")
        user_input = input(' -> ')
        if user_input == "exit":
            client_socket.close()
            return
        else:
            user_input = int(user_input) + 7

        client_socket.send(str.encode(str(user_input)))
    elif code == "4":
        print("Username already exists. Please try again.\n")
        # Send welcome menu code to server
        client_socket.send(str.encode("0"))
    elif code == "5":
        print("Username does not exist.\n")
        # Send welcome menu code to server
        client_socket.send(str.encode("0"))
    elif code == "6":
        print("Incorrect Password.\n")
        # Send welcome menu code to server
        client_socket.send(str.encode("0"))
    elif code == "7":
        print("Registration success!\n")
        # Send welcome menu code to server
        client_socket.send(str.encode("0"))
    elif code == "8":
        print("\nHighscores")
        print("This feature is in development. Please check back later")
        client_socket.send(str.encode("3"))
    elif code == "9":
        print("\nGame Rules")
        print("This feature is in development. Please check back later")
        client_socket.send(str.encode("3"))
    elif code == "10":
        print("\nGame")
        print("This feature is in development. Please check back later")
        client_socket.send(str.encode("3"))
    else:
        print("Server closed connection. Please try again.\n")
        client_socket.close()


if __name__ == "__main__":
    while True:
        PORT = input("Port: ")
        try:
            PORT = int(PORT)
            break
        except ValueError:
            print("Invalid port number")
    # Get host name
    HOST = socket.gethostbyname(socket.gethostname())
    client_program(HOST, PORT)

