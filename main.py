from game import Game
from board import Board
from player import Player
from piece import Piece
from random import randint
from aima_method import SeachMethod
import time, pygame, math, thread
from pygame.locals import *


class GameLoop():        

    def game_init(self):


        ### CHOOSING PLAYER 1 ###
        print "What kind of player is Player 1 (white)? [h|r|i|f|s]"
        while True:
            user_choose_player = raw_input("where h=human, r=random bot, i=idiot bot, f=figther bot, s=smartest bot: ")
            if user_choose_player == "h":
                player_one = Player(Player.HUMAN, Piece.WHITE)
                break
            if user_choose_player == "r":
                player_one = Player(Player.RANDOM, Piece.WHITE)
                break
            if user_choose_player == "i":
                player_one = Player(Player.IDIOT, Piece.WHITE)
                break
            if user_choose_player == "f":
                player_one = Player(Player.FIGHTER, Piece.WHITE)
                break
            if user_choose_player == "s":
                player_one = Player(Player.SMARTEST, Piece.WHITE)
                break
            print "Wrong input, please, type 'h', 'r', 's', 'f' or 'i' to select a player type"


        ### CHOOSING PLAYER 2 ###
        print "\nWhat kind of player is Player 2 (black)? [h|r|i|f|s]"
        while True:
            user_choose_player = raw_input("where h=human, r=random bot, i=idiot bot, f=figther bot, s=smartest bot: ")
            if user_choose_player == "h":
                player_two = Player(Player.HUMAN, Piece.BLACK)
                break
            if user_choose_player == "r":
                player_two = Player(Player.RANDOM, Piece.BLACK)
                break
            if user_choose_player == "i":
                player_two = Player(Player.IDIOT, Piece.BLACK)
                break
            if user_choose_player == "f":
                player_two = Player(Player.FIGHTER, Piece.BLACK)
                break
            if user_choose_player == "s":
                player_two = Player(Player.SMARTEST, Piece.BLACK)
                break
            print "Wrong input, please, type 'h', 'r', 's', 'f' or 'i' to select a player type"

        ### CREATING THE GAME INSTANCE ###
        game = Game(player_one, player_two)

        ### CHOOSING THE BOARD ###
        print "\nFor Default Board -> d, Black Wins Board -> b, King vs King and rooks -> r "
        while True:
            user_board_select = raw_input()
            if user_board_select == "d":
                board = Board(6, 4)
                board.initialize_default_board()
                print "Default board loaded\n"
                break
            elif user_board_select == "b":
                board = Board(6, 4)
                board.initialize_black_one_move_win()
                print "Black Wins Board\n"
                break
            elif user_board_select == "r":
                board = Board(6, 4)
                board.initialize_king_and_rook()
                print "King vs King and rooks\n"
                break
            print '\nWrong input, please type "y" if you want to load the default or "n" if you want to define it yourself: '

        return [game, board, player_one, player_two]


    def game_control(self, game, board):
        while game.is_terminal(board) is False:

            if game.get_player_turn().get_type() is Player.RANDOM:
                posible_movements = game.successors(board, game.get_player_turn())
                random = randint(0, len(posible_movements) - 1)
                move_to_do = posible_movements[random]
                board.move_piece(move_to_do[0][0][0], move_to_do[0][0][1], move_to_do[0][1][0], move_to_do[0][1][1])
                game.change_turn()

            elif game.get_player_turn().get_type() is not Player.HUMAN:
                search = SeachMethod(SeachMethod.AIMA_ALPHABETA_SEARCH, 2)
                move = search.search(board, game)
                piece = board.get_piece_in_pos(move[0][0], move[0][1])
                print str(move[0][0]) + ", " + str(move[0][1])
                print piece.to_string()
                board.move_piece(move[0][0], move[0][1], move[1][0], move[1][1])
                game.change_turn()
            


    def game_ui_loop(self, game, board, player_one, player_two):
        ### GUI INITIALIZATION ###    
        pygame.init()
        screen = pygame.display.set_mode((len(board.get_board()[0])*60, len(board.get_board())*60), 1)
        pygame.display.set_caption('Radikal Chess')

        pieces = [{}, {}]
        pieces[0]["Rbw"] = pygame.image.load("./img/brw.png")
        pieces[0]["Bbw"] = pygame.image.load("./img/bbw.png")
        pieces[0]["Kbw"] = pygame.image.load("./img/bkw.png")
        pieces[0]["Qbw"] = pygame.image.load("./img/bqw.png")
        pieces[0]["Pbw"] = pygame.image.load("./img/bpw.png")
        pieces[0]["Rww"] = pygame.image.load("./img/wrw.png")
        pieces[0]["Bww"] = pygame.image.load("./img/wbw.png")
        pieces[0]["Kww"] = pygame.image.load("./img/wkw.png")
        pieces[0]["Qww"] = pygame.image.load("./img/wqw.png")
        pieces[0]["Pww"] = pygame.image.load("./img/wpw.png")
        pieces[0]["w"]   = pygame.image.load("./img/w.png")
        pieces[1]["Rbb"] = pygame.image.load("./img/brb.png")
        pieces[1]["Bbb"] = pygame.image.load("./img/bbb.png")
        pieces[1]["Kbb"] = pygame.image.load("./img/bkb.png")
        pieces[1]["Qbb"] = pygame.image.load("./img/bqb.png")
        pieces[1]["Pbb"] = pygame.image.load("./img/bpb.png")
        pieces[1]["Rwb"] = pygame.image.load("./img/wrb.png")
        pieces[1]["Bwb"] = pygame.image.load("./img/wbb.png")
        pieces[1]["Kwb"] = pygame.image.load("./img/wkb.png")
        pieces[1]["Qwb"] = pygame.image.load("./img/wqb.png")
        pieces[1]["Pwb"] = pygame.image.load("./img/wpb.png")
        pieces[1]["b"]   = pygame.image.load("./img/b.png")

        clock = pygame.time.Clock()
        mouse_pos = [-1, -1]
        highlighted_pos = [-1, -1]

        available_moves = []
        adviced_move = []
        available_white_moves = []
        available_black_moves = []
        reset_moves = [-1, -1, -1]
        start_time = time.time()

        ### MAIN GAME LOOP ###
        while game.is_terminal(board) is False:
            pygame.display.set_caption('Radikal Chess')
            movement = False
            while movement is False:

                clock.tick(5)
                self.display_board(screen, board, pieces, available_moves, highlighted_pos, available_white_moves, available_black_moves, adviced_move)

                for event in pygame.event.get():
                    if event.type is QUIT:                            
                        break
                    elif event.type is KEYDOWN:
                        if event.key is K_ESCAPE:
                            return
                        elif event.key is K_w:
                            #devolver los movimientos posibles de los blancos
                            if reset_moves[0] is -1:
                                for move in game.successors(board, player_one):
                                    available_white_moves.append(move[0])
                                reset_moves[0] = 0

                            elif reset_moves[0] is 0:
                                available_white_moves = []
                                reset_moves[0] = -1

                            self.display_board(screen, board, pieces, available_moves, highlighted_pos, available_white_moves, available_black_moves, adviced_move)
                        elif event.key is K_b:
                            #devolver los movimientos posibles de los negros
                            if reset_moves[1] is -1:
                                for move in game.successors(board, player_two):
                                    available_black_moves.append(move[0])
                                reset_moves[1] = 0

                            elif reset_moves[1] is 0:
                                available_black_moves = []
                                reset_moves[1] = -1

                            self.display_board(screen, board, pieces, available_moves, highlighted_pos, available_white_moves, available_black_moves, adviced_move)
                                
                        elif event.key is K_a:
                            if game.get_player_turn().get_type() is not Player.HUMAN:
                                break
                            #devolver un advice si el jugador es humano
                            if reset_moves[2] is -1:
                                search = SeachMethod(SeachMethod.AIMA_ALPHABETA_SEARCH, 2)
                                adviced_move = search.search(board, game)
                                reset_moves[2] = 0

                            elif reset_moves[2] is 0:
                                adviced_move = []
                                reset_moves[2] = -1
                                
                                                                
                    elif event.type is MOUSEBUTTONDOWN:
                        mouse_x_pos = event.pos[0]
                        mouse_y_pos = event.pos[1]
                        mouse_pos[0] = int(math.floor(mouse_y_pos / 60))
                        mouse_pos[1] = int(math.floor(mouse_x_pos / 60))
                        available_white_moves = []
                        available_black_moves = []

                        if game.get_player_turn().get_type() is Player.HUMAN:
                            if mouse_pos[0] is not -1:
                                if highlighted_pos[0] is mouse_pos[0] and highlighted_pos[1] is mouse_pos[1]:
                                    highlighted_pos[0] = -1
                                    available_moves = []
                                elif mouse_pos in available_moves:
                                    movement = board.move_piece(highlighted_pos[0], highlighted_pos[1], mouse_pos[0], mouse_pos[1])
                                    highlighted_pos[0] = -1
                                    available_moves = []
                                    game.change_turn()
                                else:
                                    piece = board.get_piece_in_pos(mouse_pos[0], mouse_pos[1])
                                    if piece is not None:
                                        if (game.get_player_turn() is player_one and piece.get_color() is Piece.WHITE) or \
                                            (game.get_player_turn() is player_two and piece.get_color() is Piece.BLACK):
                                            highlighted_pos[0] = mouse_pos[0]
                                            highlighted_pos[1] = mouse_pos[1]
                                            available_moves = board.is_legal_movement(mouse_pos[0], mouse_pos[1])

        self.display_board(screen, board, pieces, available_moves, highlighted_pos, available_white_moves, available_black_moves, adviced_move)
        pygame.display.set_caption(str(game.get_player_turn().to_string() + ", YOU HAVE BEEN DEFEATED!"))

        print board.to_string()


    @staticmethod
    def display_board(screen, board, pieces, available_moves, highlighted_pos, available_white_moves, available_black_moves, adviced_move):
        i = 0
        for x in range(len(board.get_board()[0])):
            j = 0         
            for y in range(len(board.get_board())):
                piece = board.get_piece_in_pos(y, x)
                square_color = "w"                
                if (i+j)%2 is 1:
                    square_color = "b"
                if piece is not None:
                    screen.blit(pieces[(i+j)%2][str(piece.to_string() + square_color)], (i*60, j*60))
                    pygame.display.update()
                else:
                    screen.blit(pieces[(i+j)%2][str(square_color)], (i*60, j*60))
                    pygame.display.update()
                j += 1
            i += 1

        pos_rect = pygame.Rect(0, 0, 60, 60)

        if highlighted_pos[0] is not -1:
            pos_rect.left = highlighted_pos[1]*60
            pos_rect.top = highlighted_pos[0]*60
            pygame.draw.rect(screen, (115, 102, 255), pos_rect, 4)

        for pos in available_moves:
            pos_rect.left = pos[1]*60
            pos_rect.top = pos[0]*60
            pygame.draw.rect(screen, (115, 102, 255), pos_rect, 4)

        for pos in adviced_move:
            pos_rect.left = pos[1]*60
            pos_rect.top = pos[0]*60
            pygame.draw.rect(screen, (0, 255, 0), pos_rect, 4)

        for pos in available_white_moves:
            pos_rect.left = pos[0][1]*60
            pos_rect.top = pos[0][0]*60
            pygame.draw.rect(screen, (255, 255, 255), pos_rect, 4)
            pos_rect.left = pos[1][1]*60
            pos_rect.top = pos[1][0]*60
            pygame.draw.rect(screen, (255, 255, 255), pos_rect, 4)

        for pos in available_black_moves:
            pos_rect.left = pos[0][1]*60
            pos_rect.top = pos[0][0]*60
            pygame.draw.rect(screen, (100, 100, 100), pos_rect, 4)
            pos_rect.left = pos[1][1]*60
            pos_rect.top = pos[1][0]*60
            pygame.draw.rect(screen, (100, 100, 100), pos_rect, 4)

        pygame.display.flip()


def main():
    g = GameLoop()
    params = g.game_init()
    try:
        thread.start_new_thread(g.game_ui_loop, (params[0], params[1], params[2], params[3]))
        thread.start_new_thread(g.game_control, (params[0], params[1]))
    except:
        print "Thread unable to start"
    while 1:
        continue



    


if __name__ == '__main__':
    main()