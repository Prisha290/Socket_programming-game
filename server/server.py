import sys
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

        # Global Context requirement
        self.room = 0  # room space
        self.higher_score = []  # to store higher score in a game for players
        self.high_scores = []  # to store global high scores
        self.difficulty_list = []  # to store the game difficulty

        # Mutex requirement
        self.mutex_lock = threading.Lock()  # a thread lock
        self.is_running = True  # flag to show if current thread is running

    def startup(self):
        """startup the server"""
        while True:
            print("[SERVER] Started ...")
            soc, addr = self.server_socket.accept()
            print('[SERVER] Client Connection received: ', addr)

            client_soc = SocketWrapper(soc)  # init the client sockets

            Thread(target=lambda: self.request_handle(client_soc)).start()

    def register_service(self, request_id, handle_function):
        """register services according to the protocol code"""
        self.request_handle_function[request_id] = handle_function

    def request_handle(self, client_soc):
        """Create a new thread for receiving data from the client """
        while self.is_running:
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
        print("[SERVER] REQUEST SELECT-DIFFICULTY RECEIVED.")
        difficulty = request_data['difficulty']

        int_difficulty = int(difficulty)

        self.mutex_lock.acquire()  # add mutex
        self.difficulty_list.append(int_difficulty)  # append difficulties to list
        self.mutex_lock.release()  # release mutex

        while len(self.difficulty_list) < 2:
            time.sleep(0.1)

        response_difficulty = str(self.difficulty_list[0])
        print('[SERVER] Serializing Response Difficulty data ...')
        response_text = ResponseProtocol.response_send_difficulty(response_difficulty)
        client_soc.send_data(response_text)
        print("[SERVER] RESPONSE SELECT DIFFICULTY SENT.")

    def request_register_handle(self, client_soc, request_data):
        """Handle the register request from the client"""
        print("[SERVER] REQUEST REGISTER RECEIVED.")
        username = request_data['username']
        password = request_data['password']
        result, username = self.register_user(username, password)
        if result == '0':
            print('[SERVER] Serializing Response Registration Data...')
            response_text = ResponseProtocol.response_register_result(result, username)
            client_soc.send_data(response_text)
            print("[SERVER] RESPONSE REGISTER SENT.")

    def register_user(self, username, password):
        """Register user to database"""
        auth.add_user(username, password)
        print("[SERVER] REGISTRATION SUCCESS FOR\n[USER]: ", username, end='')
        print('\n[Hashed password]: ', auth.hash_password(password))
        return '0', username

    def request_login_handle(self, client_soc, request_data):
        """Handle the login request from the server"""
        print("[SERVER] REQUEST LOGIN RECEIVED.")
        username = request_data['username']
        password = request_data['password']
        result, username = self.check_user_login(username, password)
        if result == '0':
            self.clients[username] = {'sock': client_soc, 'username': username}

            print('[SERVER] Current login players: ', end=' ')
            names = list(self.clients.keys())
            for name in names:
                print(name, end=', ')
            print()
        print('[SERVER] Serializing Response Login Data...')
        response_text = ResponseProtocol.response_login_result(result, username)
        client_soc.send_data(response_text)
        print("[SERVER] RESPONSE LOGIN SENT.")

    def check_user_login(self, username, password):
        """Check the user login"""
        # check if username in users.json
        if not auth.check_user_exist(username):
            # -1 user not exits
            return '-1', username
            # username or password wrong
        if not auth.check_user_password(username, password):
            return '-2', username
        return '0', username

    def request_show_rule_handle(self, client_soc, request_data):
        """Handle the show-rules request from server"""
        print("[SERVER] REQUEST SHOW-RULES RECEIVED.")
        rules = ""
        rules += "\n🧚 GAME RULES\n"
        rules += "\n🚩 Display:"
        rules += "\nEach game, your position in the maze is indicated by 🏃 and 🏁 indicates the exit.\n"
        rules += "\n🚩 Instructions"
        rules += ("\n\" W\" to go ⬆\n \"A\" to go ⬅\n \"S\" to go ⬇\n "
                  + "\"D\" to go ➡ \nYou won't be able to move if you hit "
                  + "a wall. \nYour goal is to reach the exit point 🤩\n")
        rules += "\n🚩 Scores:"
        rules += ("\nThe time you spent on each round is your score. \nA ⏰ "
                  + "will start when the game begins and stop as soon as you "
                  + "reach the exit point. \nYour best score 🏅 will be updated to "
                  + "the record board 💯 where you may visit from Game Menu.")

        print('[SERVER] Serializing Response Show Rules Data...')
        response_text = ResponseProtocol.response_show_rule_result(rules)
        client_soc.send_data(response_text)
        print("[SERVER] RESPONSE SHOW-RULES SENT.")

    def request_play_game_handle(self, client_soc, request_data):
        """Handle the play-game request from the client"""
        print("[SERVER] REQUEST PLAY-GAME-2PLAYER RECEIVED.")

        self.mutex_lock.acquire()  # add mutex lock the room
        self.room += 1  # update room
        self.mutex_lock.release()  # release mutex lock

        """0004|number of players in room"""
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
            print("[SERVER] RESPONSE SELECT-2PLAY-GAME SENT.")

    def command_start_game(self, client_soc):
        """Request client to start the game"""
        print('[SERVER] Serializing Response Start Game Data...')
        response_text = ResponseProtocol.command_start_game()
        client_soc.send_data(response_text)
        print("[SERVER] RESPONSE START-2PLAYER-GAME SENT.")

    def request_send_score_handle(self, client_soc, request_data):
        """Handle the send-score-request from the client """
        print("[SERVER] REQUEST SEND-SCORE RECEIVED.")
        score = request_data['score']
        float_score = float(score)

        self.mutex_lock.acquire()  # Add mutex lock
        self.higher_score.append(float_score)
        self.mutex_lock.release()   # release the lock

        while len(self.higher_score) < 2:
            time.sleep(0.5)

        self.higher_score.sort()

        # add to high scores board
        self.mutex_lock.acquire()  # add mutex lock
        self.high_scores.append(float_score)   # append scores to score board
        self.mutex_lock.release()  # release mutex lock
        self.high_scores.sort()  # sort the scores in ascending order

        response_score = self.higher_score[0]
        self.room = 0
        print('[SERVER] Serializing Response Send Score Data...')
        response_text = ResponseProtocol.response_send_score(str(response_score))
        client_soc.send_data(response_text)
        print("[SERVER] RESPONSE SCORE SENT.")

    def request_high_scores_handle(self, client_soc, request_data):
        """Handle the high-score request from the client"""
        print("[SERVER] REQUEST SHOW-HIGH-SCORES RECEIVED.")
        message = ""
        for i in range(len(self.high_scores)):
            message += str(self.high_scores[i]) + "\n"
        print('[SERVER] Serializing Response High Scores Data...')
        response_text = ResponseProtocol.response_high_score(message)
        client_soc.send_data(response_text)
        print("[SERVER] RESPONSE HIGH-SCORES SENT.")

    def remove_offline_user(self, client_soc):
        """Remove offline users"""
        for username, info in self.clients.items():
            if info['sock'] == client_soc:
                print('[SERVER] Client ' + info['username'] + ' Logout.')
                del self.clients[username]
                break
        print('[SERVER] Current online clients: ', end=' ')
        if not self.clients:
            print("All clients logged out.")
        names = list(self.clients.keys())
        for name in names:
            print(name, end=', ')
        print()

    def parse_request_text(self, text):
        """Deserialize the request from the client"""
        print('[SERVER] Deserializing Request Data from client...')
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

    def request_exit(self, client_soc):
        request_data = ResponseProtocol.request_exit()
        client_soc.send_data(request_data)
        print("[SERVER] INFORM EXIT SENT.")

    def exit(self):
        """Server Disconnect"""
        for client_soc in self.clients.values():
            self.request_exit(client_soc)
            client_soc.close()

        self.server_socket.close()
        self.is_running = False
        print("[SERVER DISCONNECTED]")
        sys.exit(0)


if __name__ == '__main__':
    server = Server()
    try:
        server.startup()
    except KeyboardInterrupt:
        server.exit()
