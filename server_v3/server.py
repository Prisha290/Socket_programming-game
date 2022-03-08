import threading
import time
from threading import Thread

import auth
from response_protocol import *
from server_socket import ServerSocket
from socket_wrapper import SocketWrapper


class Server(object):
    def __init__(self):
        self.server_socket = ServerSocket()  # init a server socket

        # register service for the requests and responses
        self.request_handle_function = dict()
        self.register_service(REQUEST_LOGIN, self.request_login_handle)
        self.register_service(REQUEST_REGISTER, self.request_register_handle)
        self.register_service(REQUEST_SHOW_RULE, self.request_show_rule_handle)
        self.register_service(REQUEST_PLAY_GAME, self.request_play_game_handle)
        self.register_service(REQUEST_SEND_SCORE, self.request_send_score_handle)
        self.register_service(REQUEST_HIGH_SCORES, self.request_high_scores_handle)
        self.register_service(REQUEST_SEND_DIFFICULTY, self.request_send_difficulty_handle)

        self.clients = dict()  # to store online clients
        self.room = 0  # room space
        self.higher_score = []  # to store higher score in a game for play 1 amd 2
        self.high_scores = []  # to store global high scores
        self.difficulty_list = []  # to store the game difficulty
        self.mutex_lock = threading.Lock()  # a thread lock

    def startup(self):
        """startup the server"""
        while True:
            print("Connecting to client...")
            soc, addr = self.server_socket.accept()
            print('Accepted', addr)

            client_soc = SocketWrapper(soc)  # init the client sockets

            Thread(target=lambda: self.request_handle(client_soc)).start()

    def register_service(self, request_id, handle_function):
        """register services according to the protocol code"""
        self.request_handle_function[request_id] = handle_function

    def request_handle(self, client_soc):
        """Create a new thread for receiving data from the client """
        while True:
            recv_data = client_soc.recv_data()
            if not recv_data:
                self.remove_offline_user(client_soc)
                client_soc.close()
                break

            parse_data = self.parse_request_text(recv_data)

            handle_function = self.request_handle_function.get(parse_data['request_id'])
            if handle_function:
                handle_function(client_soc, parse_data)

    def request_send_difficulty_handle(self, client_soc, request_data):
        """Handle the send-difficulty request from the server"""
        print("REQUEST SELECT DIFFICULTY RECEIVED")
        difficulty = request_data['difficulty']

        int_difficulty = int(difficulty)

        self.mutex_lock.acquire()
        self.difficulty_list.append(int_difficulty)
        self.mutex_lock.release()
        while len(self.difficulty_list) < 2:
            time.sleep(0.1)

        response_difficulty = str(self.difficulty_list[0])

        print("send diff", response_difficulty)

        response_text = ResponseProtocol.response_send_difficulty(response_difficulty)
        client_soc.send_data(response_text)
        print("RESPONSE SELECT DIFFICULTY SENT")

    def request_register_handle(self, client_soc, request_data):
        """Handle the register request from the client"""
        username = request_data['username']
        password = request_data['password']
        result, username = self.register_user(username, password)
        if result == '0':
            response_text = ResponseProtocol.response_register_result(result, username)
            client_soc.send_data(response_text)

    def register_user(self, username, password):
        """Register user to database"""
        auth.add_user(username, password)
        print("[REGISTER SUCCESS FOR]", username)
        return '0', username

    def request_login_handle(self, client_soc, request_data):
        """Handle the login request from the server"""
        username = request_data['username']
        password = request_data['password']
        result, username = self.check_user_login(username, password)
        if result == '0':
            self.clients[username] = {'sock': client_soc, 'username': username}

            print('Current online client: ', self.clients)

        response_text = ResponseProtocol.response_login_result(result, username)
        client_soc.send_data(response_text)

    def check_user_login(self, username, password):
        """Check the user login"""
        # check if username in users.json
        if not auth.check_user_exist(username):
            print('not exist')
            # -1 user not exits
            return '-1', username
            # username or password wrong
        if not auth.check_user_password(username, password):
            return '-2', username
        return '0', username

    def request_show_rule_handle(self, client_soc, request_data):
        """Handle the show-rules request from server"""
        rules = ""
        rules += "Game Rules\n"
        rules += "\nDisplay:"
        rules += "\nEach game, your position in the maze is indicated by 🏃\n 🏁 indicates the exit.\n"
        rules += "\nInstructions:"
        rules += ("\nPress \"W\" to go up, \"A\" to go left, \"S\" to go down, "
                  + "and \"D\" to go right. You\nwon't be able to move if you hit "
                  + "a wall. Your goal is to reach the exit point\n")
        rules += "\nScores:"
        rules += ("\nThe time you spent on each round is your score. A timer "
                  + "will start when the\ngame begins and stop as soon as you "
                  + "reach the exit point. Your best score\nwill be updated to "
                  + "the record board where you may visit from Game Menu.")

        result = '0'
        response_text = ResponseProtocol.response_show_rule_result(rules)
        client_soc.send_data(response_text)

    def request_play_game_handle(self, client_soc, request_data):
        """Handle the play-game request from the client"""
        self.room += 1
        """0004|num of player in room"""
        if self.room == 1:

            response_text = ResponseProtocol.response_play_game_result('1')
            client_soc.send_data(response_text)
            while True:
                time.sleep(0.1)
                if self.room == 2:
                    response_text = ResponseProtocol.response_play_game_result('2')
                    client_soc.send_data(response_text)
                    break


        else:
            response_text = ResponseProtocol.response_play_game_result('2')
            client_soc.send_data(response_text)

    def command_start_game(self, client_soc):
        """Request client to start the game"""
        response_text = ResponseProtocol.command_start_game()
        client_soc.send_data(response_text)

    def request_send_score_handle(self, client_soc, request_data):
        """Handle the send-score-request from the client """
        score = request_data['score']
        float_score = float(score)

        # Add mutex lock
        self.mutex_lock.acquire()
        self.higher_score.append(float_score)

        # release the lock
        self.mutex_lock.release()

        while len(self.higher_score) < 2:
            time.sleep(0.5)

        self.higher_score.sort()

        # add to high scores board
        self.high_scores.append(float_score)
        self.high_scores.sort()

        response_score = self.higher_score[0]
        self.room = 0

        response_text = ResponseProtocol.response_send_score(str(response_score))
        client_soc.send_data(response_text)

    def request_update_record(self):
        """pass"""
        self.higher_score.clear()
        self.high_scores.append(self.higher_score[0])
        self.high_scores.append(self.higher_score[1])

        self.high_scores.sort()
        self.room = 0
        self.higher_score = []

    def request_high_scores_handle(self, client_soc, request_data):
        """Handle the high-score request from the client"""
        message = ""
        for i in range(len(self.high_scores)):
            message += str(self.high_scores[i]) + "\n"
        response_text = ResponseProtocol.response_high_score(message)
        client_soc.send_data(response_text)

    def remove_offline_user(self, client_soc):
        """Remove offline users"""
        print('A client logout.')
        for username, info in self.clients.items():
            if info['sock'] == client_soc:
                del self.clients[username]
                print(self.clients)
                break

    def parse_request_text(self, text):
        """Deserialize the request from the client"""
        request_list = text.split(DELIMITER)

        request_data = dict()
        request_data['request_id'] = request_list[0]

        if request_data['request_id'] == REQUEST_LOGIN:

            request_data['username'] = request_list[1]
            request_data['password'] = request_list[2]

        elif request_data['request_id'] == REQUEST_REGISTER:

            request_data['username'] = request_list[1]
            request_data['password'] = request_list[2]

        elif request_data['request_id'] == REQUEST_SEND_SCORE:
            request_data['score'] = request_list[1]

        elif request_data['request_id'] == REQUEST_SEND_DIFFICULTY:
            request_data['difficulty'] = request_list[1]

        return request_data


if __name__ == '__main__':
    server = Server()
    server.startup()
