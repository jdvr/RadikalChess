import json


class Save(object):
    FILE = "Save a game in a file"
    DATA_BASE = "Save a game in the data base for utility"

    def __init__(self, game_id):
        self.__output = dict()
        self.__output['id'] = game_id

    def add_players(self, player_one, player_two):
        self.__output['playerone'] = player_one.to_json()
        self.__output['playertwo'] = player_two.to_json()

    def add_board(self, board):
        self.__output['state'] = board

    def add_winner(self, winner):
        self.__output['winner'] = winner.to_json()

    def dump_to(self, mode):
        if mode is self.FILE:
            f = open(str(self.__output['id']), 'w')
            f.write(json.dumps(self.__output))
        else:
            f = open('db.games', 'a')
            f.write(json.dumps(self.__output) + '\n')

