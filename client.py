import socket
import getpass # for password input
import auth
# from dotenv import load_dotenv

# env_host = config('HOST')
# env_port = config('PORT')
# print(env_host, env_port)

def client_program():
    try: 
        # get host name
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 5050

        # Socket instance
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        client_socket.connect((HOST, PORT))

        # Receive Welcome message
        response = client_socket.recv(2048).decode()
        print(response)
        # Receive Welcome Menu code from server
        response = client_socket.recv(2048).decode()
        # Print Welcome Menu
        menu_code(response, client_socket)
        
        # Receive next menu code from server
        while response:
            response = client_socket.recv(2048).decode()
            print(response)
            menu_code(response, client_socket)
    except OSError as e:
        print('Goodbye!')


    # while message.lower().strip() != 'exit':
    #   client_socket.send(message.encode())
    #   data = client_socket.recv(1024).decode()

    #   print("Received from server: ", data)

    #   message = input(' -> ')
    # client_socket.close()

def menu_code(code, client_socket):
    if code == "0":
        print("Press 1 to Login")
        print("Press 2 to Register")
        print("Type exit to disconnect")
        user_input = input(' -> ')
        if user_input == "exit":
            client_socket.close()
            return
        client_socket.send(str.encode(user_input))
    elif code == "1":
        print("Login dialog")
        
        username = input("Username: ")
        while auth.check_username(username) == False:
            print("Username must be at least 3 characters long and all lowercase")
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

    elif code == "2":
        print("Registration dialog")

        username = input("Username: ")
        while auth.check_username(username) == False:
            print("Username must be at least 3 characters long and all lowercase")
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
        # password = input("Password: ")
        client_socket.send(str.encode(password))

    elif code == "3":
        print("Welcome to Maze Runner")
        print("Press 1 to see highscores")
        print("Press 2 to see game rules")
        print("Press 3 to play/view a game")
        print("Type exit to disconnect")
        user_input = input(' -> ')
        if user_input == "exit":
            client_socket.close()
            return
        client_socket.send(str.encode(user_input))
    elif code == "4":
        print("Username already exists. Please try again.\n")
        # Show the welcome menu again
        menu_code("0", client_socket)
    elif code == "5":
        print("Username does not exist.\n")
        # Show the welcome menu again
        menu_code("0", client_socket)
    else:
        print("Server error. Please try again.\n")
        client_socket.close()


if __name__ == "__main__":
    client_program()

