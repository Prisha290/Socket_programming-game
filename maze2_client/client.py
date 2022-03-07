from threading import Thread

from Maze import *
from Timer import *
from client_socket import ClientSocket
from config import *
from request_protocol import RequestProtocol


class Client(object):

    def __init__(self):

        self.conn = ClientSocket()


        self.response_handle_function = {}
        self.register_service(RESPONSE_LOGIN_RESULT, self.response_login_handle)
        self.register_service(RESPONSE_REGISTER_RESULT, self.response_register_handle)
        self.register_service(RESPONSE_SHOW_RULE_RESULT, self.response_show_rule_handle)
        self.register_service(RESPONSE_PLAY_GAME, self.response_play_game_handle)
        self.register_service(COMMAND_START, self.command_start_handle)
        self.register_service(RESPONSE_SEND_SCORE, self.response_send_score_handle)
        self.register_service(RESPONSE_HIGH_SCORES, self.response_high_score_handle)


        self.username = None


        self.is_running = True
        self.my_time_elapsed = 0

    def register_service(self, request_id, handle_function):

        self.response_handle_function[request_id] = handle_function

    def startup(self):

        self.conn.connect()

        Thread(target=self.response_handle).start()
        self.show_welcome_info()

    def send_register_data(self):
        username = input('Username: ')
        password = input('Password: ')
        self.username = username


        request_text = RequestProtocol.request_register_result(username, password)


        self.conn.send_data(request_text)

    def send_login_data(self):

        username = input('Username: ')
        password = input('Password: ')


        request_text = RequestProtocol.request_login_result(username, password)



        self.conn.send_data(request_text)

    def request_show_rule(self):
        request_text = RequestProtocol.request_show_rule_result()
        self.conn.send_data(request_text)

    def request_play_game(self):
        request_text = RequestProtocol.request_play_game_result()
        self.conn.send_data(request_text)

    def response_handle(self):

        while self.is_running:

            recv_data = self.conn.recv_data()

            response_data = self.parse_response_data(recv_data)

            handle_function = self.response_handle_function[response_data['response_id']]

            if handle_function:
                handle_function(response_data)

    def request_high_scores(self):
        response_text = RequestProtocol.request_high_scores()
        self.conn.send_data(response_text)

    def response_high_score_handle(self, response_data):
        result = response_data['result']
        if not result:
            print("Score Board is Empty Currently")
        else:
            print(result)
        self.prompt_player()

    @staticmethod
    def parse_response_data(recv_data):

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

        return response_data

    def response_login_handle(self, response_data):

        result = response_data['result']
        if result == '-1':
            print('[LOGIN FAILED] Username does not exist')
            self.show_welcome_info()
        elif result == '-2':
            print('[LOGIN FAILED] Password is incorrect')
            self.show_welcome_info()
        elif result == '0':
            self.prompt_player()

    def prompt_player(self):
        print('\n')
        print("=============================")
        print("| Press 1 to see high scores |")
        print("| Press 2 to see game rules  |")
        print("| Press 3 to play a game     |")
        print("| Type exit to disconnect    |")
        print("==============================")
        user_input = input(' -> ')
        if user_input == 'exit':
            self.conn.close()
        elif user_input == '1':
            self.request_high_scores()
        elif user_input == '2':
            self.request_show_rule()
        elif user_input == '3':
            self.request_play_game()
        else:
            self.prompt_player()

    def response_register_handle(self, response_data):
        result = response_data['result']
        if result == '0':
            print('[REGISTER SUCCESS]')
            self.show_welcome_info()

    def response_show_rule_handle(self, response_data):
        game_rule = response_data['result']
        print(game_rule)
        self.prompt_player()

    def response_play_game_handle(self, response_data):
        result = response_data['result']
        if result == '1':
            print('Waiting another player to join the room...')

        elif result == '2':
            print("two players joined room")
            self.command_start_handle(response_data)

    def command_start_handle(self, response_data):
        timer = Timer()
        timer.start()
        Maze().startup()
        elapsed = timer.stop()
        print("Total Time: ", elapsed)
        self.my_time_elapsed = elapsed
        self.send_game_score(elapsed)

    def send_game_score(self, score):
        request_text = RequestProtocol.request_send_score(str(score))
        self.conn.send_data(request_text)

    def response_send_score_handle(self, response_data):
        result = response_data['result']
        message = ''
        if str(self.my_time_elapsed) == result:
            message += "You won!"

        else:
            message += "You lost, the winner's total time is " + result + ' second.'
        print(message)
        self.prompt_player()

    def show_welcome_info(self):
        print('============================')
        print('|   Welcome Menu            |')
        print('|   Press 1 to Login        |')
        print('|   Press 2 to Register     |')
        print('|   Type exit to disconnect |')
        print('=============================')

        request_handle = input('-> ')
        if request_handle == '1':
            self.send_login_data()
        elif request_handle == '2':
            self.send_register_data()
        elif request_handle == 'exit' or not request_handle:
            self.conn.close()


if __name__ == '__main__':
    client = Client()
    client.startup()
