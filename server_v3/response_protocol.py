from config import *


class ResponseProtocol(object):
    @staticmethod
    def response_login_result(result, username):
        """1001|0|Youjin"""
        return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, username])

    @staticmethod
    def response_register_result(result, username):
        """1002|0|Youjin"""
        return DELIMITER.join([RESPONSE_REGISTER_RESULT, result, username])

    @staticmethod
    def response_show_rule_result(rule):
        """1003|Game Rules"""
        return DELIMITER.join([RESPONSE_SHOW_RULE_RESULT, rule])

    @staticmethod
    def response_play_game_result(result):
        """1004|0"""
        return DELIMITER.join([RESPONSE_PLAY_GAME, result])

    @staticmethod
    def command_start_game():
        """1005"""
        return DELIMITER.join([COMMAND_START])

    @staticmethod
    def response_send_score(score):
        """1006|16.5 Second"""
        return DELIMITER.join([RESPONSE_SEND_SCORE, score])

    @staticmethod
    def response_high_score(message):
        """1007|9 Second"""
        return DELIMITER.join([RESPONSE_HIGH_SCORES, message])

    @staticmethod
    def response_send_difficulty(difficulty):
        """1009|Easy"""
        return DELIMITER.join([RESPONSE_SEND_DIFFICULTY, difficulty])

    @staticmethod
    def request_exit():
        """1010"""
        return DELIMITER.join([REQUEST_EXIT])
