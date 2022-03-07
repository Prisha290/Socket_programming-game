from config import *


class ResponseProtocol(object):


    @staticmethod
    def response_login_result(result, username):
        return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, username])

    @staticmethod
    def response_register_result(result, username):
        return DELIMITER.join([RESPONSE_REGISTER_RESULT, result, username])

    @staticmethod
    def response_show_rule_result(rule):
        return DELIMITER.join([RESPONSE_SHOW_RULE_RESULT, rule])

    @staticmethod
    def response_play_game_result(result):
        return DELIMITER.join([RESPONSE_PLAY_GAME, result])

    @staticmethod
    def command_start_game():
        return DELIMITER.join([COMMAND_START])

    @staticmethod
    def response_send_score(score):
        return DELIMITER.join([RESPONSE_SEND_SCORE, score])

    @staticmethod
    def response_high_score(message):
        return DELIMITER.join([RESPONSE_HIGH_SCORES, message])
