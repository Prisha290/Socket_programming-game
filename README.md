# Maze Runner
A Python Client/Server Maze Runner multiplayer game

## Created by **Nirmalya, Youjin, James,** and **Yvonne** for CPSC 5042 @ SeattleU | Winter 2022

The goal of this project was to create a client-server project with threading and thread synchronization. The server can handle multiple clients at once with the help of threads. Server is fault tolerant, i.e., it is able to handle bad input from the user. Every user would need to create an account and login to play the game. User credentials are stored on the backed in a JSON file. The passwords are encrypted and there is no way of retrieving it if forgotten.

There is a _config.py_ file in the server and client folder. Please update the **SERVER_IP** and the **SERVER_PORT** number to match so the connection between the server and the client can be made successfully.

A client would not be able to connect to a server if the server is down/not running. 

The entire program is command-line based so everyone will have to interact using a terminal via a keyboard. 

## Running the project
Clone this repository

### Running the server
- Navigate to server folder and run `python3 server.py`
- This starts the server and the server is listening for client connections

### Running the client
- Navigate to client folder in a new terminal window and run `python3 client.py`
- You should be connected to the server. 
- Follow the prompts and interact with the program!


Thank you for checking our project! 
