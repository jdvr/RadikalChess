__author__ = 'JuanDavid'

from player import Player
from game import Game
from board import Board
from piece import Piece
from aima_method import SeachMethod
from random import randint
from load import Load
import json

p_one = Player(Player.RANDOM, Piece.WHITE)
p_two = Player(Player.SMARTEST, Piece.BLACK)

game = Game(p_one, p_two)
board = Board(6, 4)
board.initialize_default_board()
print "Que empieze el juego"

while game.is_terminal(board) is False:

    posible_movements = game.successors(board, game.get_player_turn())
    search = SeachMethod(SeachMethod.AIMA_ALPHABETA_SEARCH, 1)
    move = search.search(board, game)
    print board.get_piece_in_pos(move[0][0], move[0][1]).to_string()
    board.move_piece(move[0][0], move[0][1], move[1][0], move[1][1])
    game.change_turn()
    print board.to_string()

game.to_db(board, game.get_enemy_player())