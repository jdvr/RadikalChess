__author__ = 'JuanDavid'

from game import Game
from board import Board
from player import Player
from piece import Piece
from random import randint
from aima_method import SeachMethod
import os
import time
import random


class Stats(object):
    def __init__(self, gm, game_number):
        self.__stats = dict()
        self.__stats['id'] = self.__hash__()
        self.__stats['game_number'] = game_number
        self.__stats['p1'] = gm.get_player_one().get_type()
        self.__stats['p2'] = gm.get_player_two().get_type()

    def add_expanded_nodes(self, player, nodes):
        if player.get_color() is Piece.WHITE:
            if 'p1_exp' in self.__stats:
                self.__stats['p1_exp'] += nodes
            else:
                self.__stats['p1_exp'] = nodes
        else:
            if 'p2_exp' in self.__stats:
                self.__stats['p2_exp'] += nodes
            else:
                self.__stats['p2_exp'] = nodes

    def add_visit_nodes(self, player):
        if player is Piece.WHITE:
            if 'p1_visit' in self.__stats:

                self.__stats['p1_visit'] += 1
            else:
                self.__stats['p1_visit'] = 1
        else:
            if 'p2_visit' in self.__stats:
                self.__stats['p2_visit'] += 1
            else:
                self.__stats['p2_visit'] = 1

    def set_game_time(self, tm):
        self.__stats['time'] = tm

    def set_winner(self, player):
        self.__stats['winner'] = player

    def set_search_method(self, method):
        self.__stats['search_method'] = method

    def to_string(self):
        res = "id and number of game: "+ str(self.__stats['id']) + " Game Number: " + str(self.__stats['game_number']) + "\n"
        res += "time of game: " + str(self.__stats['time']) + "\n"
        res += "Player 1" + self.__stats['p1'] + "\n"
        res += "Player 2" + self.__stats['p2'] + "\n"
        res += "Player 1 visit nodes: " + str(self.__stats['p1_visit']) + "\n"
        res += "Player 2 visit nodes: " + str(self.__stats['p2_visit']) + "\n"
        res += "Player 1 exp nodes for play: " + str(self.__stats['p1_exp'] / self.__stats['p1_visit']) + "\n"
        res += "Player 2 exp nodes for play: " + str(self.__stats['p2_exp'] / self.__stats['p2_visit']) + "\n"
        res += "Winner " + self.__stats['winner'].to_string() + "\n"
        res += "Search Method " + self.__stats['search_method'] + "\n"
        return res




players = [Player.FIGHTER, Player.SMARTEST, Player.IDIOT]
### CHOOSING PLAYER 1 ###
for x in xrange(30):
    if x < 10:
        player_one = Player(players[0], Piece.WHITE)
        player_two = Player(players[1], Piece.BLACK)
    elif x < 10:
        player_one = Player(players[1], Piece.WHITE)
        player_two = Player(players[2], Piece.BLACK)
    elif x < 30:
        player_one = Player(players[2], Piece.WHITE)
        player_two = Player(players[0], Piece.BLACK)

    ### CREATING THE GAME INSTANCE ###
    game = Game(player_one, player_two)

    ### CHOOSING THE BOARD ###
    board = Board(6, 4)
    board.initialize_king_and_rook()

    game_stats = Stats(game, x)
    ### MAIN GAME LOOP ###
    start = time.time()
    while game.is_terminal(board) is False:
        search = SeachMethod(SeachMethod.AIMA_ALPHABETA_SEARCH, 2)
        game_stats.set_search_method(SeachMethod.AIMA_ALPHABETA_SEARCH)
        move = search.search(board, game)
        game_stats.add_expanded_nodes(game.get_player_turn(), search.get_expand_nodes())
        board.move_piece(move[0][0], move[0][1], move[1][0], move[1][1])
        game_stats.add_visit_nodes(game.get_player_turn().get_color())
        game.change_turn()
        print board.to_string()

    game_stats.set_game_time(time.time() - start)
    print game.get_player_turn().to_string() + ", YOU HAVE BEEN DEFEATED!"
    game_stats.set_winner(game.get_player_turn())

    ### CREATING THE GAME INSTANCE ###
    game = Game(player_two, player_one)


    ### CHOOSING THE BOARD ###
    board = Board(6, 4)
    board.initialize_king_and_rook()
    game_stats_two = Stats(game, x+1)
    start = time.time()

    while game.is_terminal(board) is False:
        search = SeachMethod(SeachMethod.AIMA_MINMAX_SEARCH, 2)
        game_stats_two.set_search_method(SeachMethod.AIMA_MINMAX_SEARCH)
        move = search.search(board, game)
        game_stats_two.add_expanded_nodes(game.get_player_turn(), search.get_expand_nodes())
        board.move_piece(move[0][0], move[0][1], move[1][0], move[1][1])
        game_stats_two.add_visit_nodes(game.get_player_turn().get_color())
        game.change_turn()
        print board.to_string()

    game_stats_two.set_game_time(time.time() - start)
    print game.get_player_turn().to_string() + ", YOU HAVE BEEN DEFEATED!"
    game_stats_two.set_winner(game.get_player_turn())

    f = open('stats_r_a_ks.txt', 'a')
    f.write(game_stats.to_string())
    f.write(game_stats_two.to_string())
    f.close()

