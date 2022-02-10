import socket
import threading
import auth
import time

class ThreadedServer(object):
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server_socket.bind((self.host, self.port))
    print("[SERVER STARTED]")

  def listen(self):
    self.server_socket.listen(5)
    while True:
      client, address = self.server_socket.accept()
      print("[CLIENT CONNECTED]", address)
      client.settimeout(60)
      threading.Thread(target = self.listen_to_client,args = (client,address)).start()
  
  def listen_to_client(self, client, address):
    client.send(str.encode("\nWelcome to the server!\n"))
    time.sleep(0.1)
    client.send(str.encode("0"))
    SIZE = 2048
    while True:
      try:
        data = client.recv(SIZE).decode()
        if not data or data == "exit":
          print("[CLIENT DISCONNECTED] Closing connection", address)
          client.close()
          break
        # Receive data from client
        if data == "1":
          """
          Login dialog
          Getting Username and Password for Login
          """
          # Send Login menu code to client
          client.send(str.encode("1"))
          # Login
          username = client.recv(SIZE).decode()
          password = client.recv(SIZE).decode()
          print(f"[LOGIN] {username} | {password}")
          # Check if username in users.json
          if auth.check_user_exist(username) == False:
            client.send(str.encode("5"))
            print("[LOGIN FAILED] Username does not exist")
          else:
            # Check if password is correct
            print("Checking password...")
            if auth.check_user_password(username, password) == False:
              client.send(str.encode("6"))
              print("[LOGIN FAILED] Password is incorrect")
            else:
              client.send(str.encode("3"))
              print("[LOGIN SUCCESS]", username)
        elif data == "2":
          """
          Register dialog
          Getting Username and Password for Registration
          """
          # Send Register menu code to client
          client.send(str.encode("2"))
          # Register
          username = client.recv(SIZE).decode()
          password = client.recv(SIZE).decode()
          print(f"[REGISTER] {username} | {password}")
          # Check if username in users.json
          if auth.check_user_exist(username) == True:
            client.send(str.encode("4"))
            print("[REGISTER FAILED] Username already exists")
          else:
            # Add user to users.json
            auth.add_user(username, password)
            client.send(str.encode("7"))
            print("[REGISTER SUCCESS]", username)
        elif data == "3":
          client.send(str.encode("3"))
        elif data == "8":
          """
          Highscores dialog
          The client will see the top 5 highscores
          """
          client.send(str.encode("8"))
        elif data == "9":
          """
          Game rules dialog
          The client will see the game rules
          """
          client.send(str.encode("9"))
        elif data == "10":
          """
          Game
          The client will play/see a game
          """
          client.send(str.encode("10"))
          
      except:
        client.close()
        return False

if __name__ == "__main__":
  while True:
    PORT = input("Port: ")
    try:
      PORT = int(PORT)
      break
    except ValueError:
      print("Invalid port number")
  HOST = socket.gethostbyname(socket.gethostname())
  ThreadedServer(HOST, PORT).listen()