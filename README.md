# Socket-programming-game (Good Computer-Networks project with OS concepts)
The goal of this project was to create a client-server project with threading and thread synchronization. The server can handle multiple clients at once with the help of threads.
Server is fault tolerant, i.e., it is able to handle bad input from the user.
Login holds good only if the players have successfully registered.
The passwords are encrypted .

There is a _config.py_ file in the server and client folder.
 **SERVER_IP** and the **SERVER_PORT** number have to match so the connection between the server and the client can be made successfully.

A client would not be able to connect to a server if the server is down/not running. 

The entire program is command-line based so everyone will have to interact using a terminal via a keyboard. 

### Running the server
- Navigate to server folder and run `python3 server.py`
- This starts the server and the server is listening for client connections

### Running the client
- Navigate to client folder in a new terminal window and run `python3 client.py`
- You should be connected to the server. 
- Follow the prompts and interact with the program!
