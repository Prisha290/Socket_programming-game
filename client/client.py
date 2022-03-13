import getpass
import sys
import os
import signal
from threading import Thread

from client_socket import ClientSocket
from config import *
from Maze import *
from Maze_Random import *
from request_protocol import RequestProtocol
from Timer import *


class Client(object):
    def __init__(self):
        self.conn = ClientSocket()  # init a client socket
        self.response_handle_function = dict()  # response handler dictionary

        # Register service for the requests and responses
        self.register_service(RESPONSE_LOGIN_RESULT,
                              self.response_login_handle)
        self.register_service(RESPONSE_REGISTER_RESULT,
                              self.response_register_handle)
        self.register_service(RESPONSE_SHOW_RULE_RESULT,
                              self.response_show_rule_handle)
        self.register_service(RESPONSE_PLAY_GAME,
                              self.response_play_game_handle)
        self.register_service(COMMAND_START, self.command_start_handle)
        self.register_service(RESPONSE_SEND_SCORE,
                              self.response_send_score_handle)
        self.register_service(RESPONSE_HIGH_SCORES,
                              self.response_high_score_handle)
        self.register_service(REQUEST_SEND_DIFFICULTY,
                              self.request_send_difficulty)
        self.register_service(RESPONSE_SEND_DIFFICULTY,
                              self.response_send_difficulty_handle)
        self.register_service(RESPONSE_EXIT, self.response_exit)

        self.username = None  # current client name
        self.is_running = True  # flag to show if current thread is running

        self.my_time_elapsed = 0  # for timer
        self.difficulty = 0  # to store game difficulty
        self.local_ranking = []  # to store local ranking

        # colors
        self.YELLOW = "\033[1;33m"
        self.END = "\033[0m"

    def register_service(self, request_id, handle_function):
        """register services according to the protocol code"""
        self.response_handle_function[request_id] = handle_function

    def response_handle(self):
        """Create a new thread for receiving data from server """
        try:
            while self.is_running:
                recv_data = self.conn.recv_data()
                response_data = self.parse_response_data(recv_data)
                handle_function = self.response_handle_function[response_data['response_id']]
                if handle_function:
                    handle_function(response_data)

        except (OSError, KeyError):
            print("Connection lost to server")
            self.exit()

    def startup(self):
        """startup the client"""
        try:
            self.conn.connect()
            # new thread for receiving data from server
            Thread(target=self.response_handle).start()
            self.show_welcome_info()
        # Handle exception when server is not online
        except ConnectionRefusedError:
            print("Server is not online. Please check back later")

    def response_exit(self, response_data):
        self.exit()

    def credentials_input(self):
        self.username = input("Username: ")
        password = getpass.getpass()
        # password = input("Password: ")

        return password

    def send_register_data(self):
        """Prompt user for username and password for registration and send them to the server"""
        password = self.credentials_input()

        request_text = RequestProtocol.request_register_result(
            self.username, password)
        self.conn.send_data(request_text)

    def send_login_data(self):
        """Prompt user for username and password for login and send them to the server"""
        password = self.credentials_input()

        request_text = RequestProtocol.request_login_result(
            self.username, password)
        self.conn.send_data(request_text)

    def request_show_rule(self):
        """Send show-game-rules request to the server """
        request_text = RequestProtocol.request_show_rule_result()
        self.conn.send_data(request_text)

    def request_play_game(self):
        """Send play-game request to the server"""
        request_text = RequestProtocol.request_play_game_result()
        self.conn.send_data(request_text)

    def request_high_scores(self):
        """Send show-high-scores request to the server """
        response_text = RequestProtocol.request_high_scores()
        self.conn.send_data(response_text)

    def response_high_score_handle(self, response_data):
        """Handle request-high-score response from the server"""
        result = response_data['result']
        print('[High Scores 🥇 🥈 🥉]')
        if not result:
            print("Score Board is Currently Empty.")
        else:
            print(result)

        self.prompt_player()

    def send_game_score(self, score):
        """Send total time taken to the server"""
        request_text = RequestProtocol.request_send_score(str(score))
        self.conn.send_data(request_text)

    def response_login_handle(self, response_data):
        """Handle the response for longin from the server"""
        result = response_data['result']
        if result == '-1':
            print('[LOGIN FAILED] Username does not exist')
            self.show_welcome_info()
        elif result == '-2':
            print('[LOGIN FAILED] Password is incorrect')
            self.show_welcome_info()
        elif result == '0':
            print('\n[LOGIN SUCCESS] Welcome Back, ' + self.username + '!')
            self.prompt_player()

    def response_register_handle(self, response_data):
        """Handle the register response from the server"""
        result = response_data['result']
        if result == '0':
            print('[REGISTER SUCCESS]')
            self.show_welcome_info()

    def response_show_rule_handle(self, response_data):
        """Handle the show-rules response from the server"""
        game_rule = response_data['result']
        print(game_rule)
        self.prompt_player()

    def response_play_game_handle(self, response_data):
        """Handle the play-game response from the server"""
        result = response_data['result']
        if result == '1':
            print('[Waiting for Player2 to Join the Room...🚀]')

        elif result == '2':
            print(
                "Two Players Joined the Room, Please Select a difficulty to play the game! 👌🥰")
            print(
                "\n[Note]: The Server will pick the difficulty level from the players who made the decision faster! 🍗")
            self.request_send_difficulty()

    def response_send_difficulty_handle(self, response_data):
        """Handle the send-difficulty response from the server"""
        print("RESPONSE SELECT DIFFICULTY RESULT HANDLED")
        result = response_data['difficulty']
        self.difficulty = int(result)

        print(result)

        if self.difficulty != 0:
            self.command_start_handle(response_data)

    def command_start_handle(self, response_data):
        """Request to start game and send the command to the server"""
        level = 'medium'  # default difficulty level
        if self.difficulty == 1:
            level = 'easy'
        elif self.difficulty == 2:
            level = 'medium'
        elif self.difficulty == 3:
            level = 'hard'
        maze = Maze(level)

        # maze = Maze_Random(int(self.difficulty))

        timer = Timer()
        timer.start()
        maze.start_game()
        elapsed = timer.stop()

        print("Total Time: ", elapsed)
        self.my_time_elapsed = elapsed
        self.send_game_score(elapsed)

    def request_send_difficulty(self):
        """Request to send a game difficulty to the server"""
        print("\nSelect Difficulty: ")
        print("1. Easy    😊")
        print("2. Medium  🤪")
        print("3. Hard    😱\n")
        # print("4. Insane (Please have a wide terminal window)")
        print(self.YELLOW, "Note: Please resize your terminal to the biggest size possible. Thanks :D", self.END)

        difficulty = input("-> ")

        while difficulty not in ['1', '2', '3']:
            print('Please Enter a valid number!')
            difficulty = input("-> ")

        request_text = RequestProtocol.request_send_difficulty(difficulty)
        self.conn.send_data(request_text)

    def response_send_score_handle(self, response_data):
        """Handle send-score response from the server"""

        result = response_data['result']
        message = ''

        if str(self.my_time_elapsed) == result:
            message += "You won! 💯 🥰"
        else:
            message += "You Lost 😭, The Winner's Total Time is " + result + ' Seconds.'
        print(message)
        self.prompt_player()

    def prompt_player(self):
        """Prompt player for actions"""
        print('\n')
        print("==================================================")
        print("|   Press 0 to see high scores [Local Ranking]   |")
        print("|   Press 1 to see high scores [Network Ranking] |")
        print("|   Press 2 to see game rules                    |")
        print("|   Press 3 to play a game 🏃 🏃 players         |")
        print("|   Press 4 to play a game 🏃 player             |")
        print("|   Type q to disconnect                         |")
        print("==================================================")

        user_input = input(' -> ')
        while user_input not in ['0', '1', '2', '3', '4', 'q']:
            print("Please Enter a Valid number: ")
            user_input = input(' -> ')
        if user_input == 'q':
            self.exit()
        elif user_input == '0':
            self.show_local_ranking()
        elif user_input == '1':
            self.request_high_scores()
        elif user_input == '2':
            self.request_show_rule()
        elif user_input == '3':
            self.request_play_game()
        elif user_input == '4':
            self.start_one_player_game()

    def show_local_ranking(self):
        """Show local game ranking"""
        print('[High Scores 🥇 🥈 🥉]')
        if not self.local_ranking:
            print('Score Board is Currently Empty.')
        else:
            for score in self.local_ranking:
                print(score)

        self.prompt_player()

    def start_one_player_game(self):
        """Start the game for one player"""
        print("\nSelect Difficulty: ")
        print("1. Easy    😊")
        print("2. Medium  🤪")
        print("3. Hard    😱\n")
        # print("4. Insane (Please have a wide terminal window)")
        print(self.YELLOW, "Note: Please resize your terminal to the biggest size possible. Thanks :D", self.END)

        difficulty = input("-> ")

        while difficulty not in ['1', '2', '3']:
            print("Please Enter a Valid Number!")
            difficulty = input("-> ")

        level = 'easy'  # default difficulty level
        if difficulty == '1':
            level = 'easy'
        elif difficulty == '2':
            level = 'medium'
        elif difficulty == '3':
            level = 'hard'

        maze = Maze(level)
        # maze = Maze_Random(int(difficulty))

        timer = Timer()
        timer.start()
        maze.start_game()
        elapsed = timer.stop()

        print("Total Time: ", elapsed)
        self.my_time_elapsed = elapsed
        self.local_ranking.append(elapsed)
        self.prompt_player()

    def show_welcome_info(self):
        """Show welcome info to the standard output """
        print('\n')
        print('============================')
        print('|  🎉 Welcome Menu 🎉      |')
        print('|  Press 1 to Login     🎲 |')
        print('|  Press 2 to Register  ⛄ |')
        print('|  Type q to disconnect 👋 |')
        print('============================')

        request_handle = input('-> ')
        while request_handle not in ['1', '2', 'q']:
            print('Please Enter a Valid Number!')
            request_handle = input('-> ')

        if request_handle == '1':
            self.send_login_data()
        elif request_handle == '2':
            self.send_register_data()
        elif request_handle == 'q' or not request_handle:
            self.exit()
        else:
            print('Please enter a valid number. 🥺')

    @staticmethod
    def parse_response_data(recv_data):
        """Parse the data from server by the Request Protocol"""
        response_data_list = recv_data.split(DELIMITER)
        response_data = dict()
        response_data['response_id'] = response_data_list[0]

        if response_data['response_id'] == RESPONSE_LOGIN_RESULT:
            response_data['result'] = response_data_list[1]
            response_data['username'] = response_data_list[2]

        if response_data['response_id'] == RESPONSE_REGISTER_RESULT:
            response_data['result'] = response_data_list[1]
            response_data['username'] = response_data_list[2]

        if response_data['response_id'] == RESPONSE_SHOW_RULE_RESULT:
            response_data['result'] = response_data_list[1]

        if response_data['response_id'] == RESPONSE_PLAY_GAME:
            response_data['result'] = response_data_list[1]

        if response_data['response_id'] == RESPONSE_SEND_SCORE:
            response_data['result'] = response_data_list[1]

        if response_data['response_id'] == RESPONSE_HIGH_SCORES:
            response_data['result'] = response_data_list[1]

        if response_data['response_id'] == RESPONSE_SEND_DIFFICULTY:
            response_data['difficulty'] = response_data_list[1]

        return response_data

    def exit(self):
        """Client Disconnect"""
        
        self.conn.close()
        self.is_running = False
        print('\nGoodbye! 👋')
        os.kill(os.getpid(), signal.SIGKILL)


if __name__ == '__main__':
    client = Client()
    client.startup()
