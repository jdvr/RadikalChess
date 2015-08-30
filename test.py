import unittest
from board import Board
from piece import Piece
from game import Game
from player import Player
import copy
import json


class Test(unittest.TestCase):
    """description of class"""

    def test_create_new_empty_board(self):
        board = Board(6, 4)
        self.assertTrue(board.is_empty())
        board_two = Board(12, 8)
        self.assertTrue(board.is_empty())
    

    def test_create_new_piece(self):
        piece = Piece(Piece.PAWN, Piece.BLACK)
        self.assertEqual('Pb', piece.to_string())


    def test_add_pieces_to_board(self):
        piece_one = Piece(Piece.PAWN, Piece.BLACK)
        piece_two = Piece(Piece.PAWN, Piece.BLACK)
        piece_three = Piece(Piece.PAWN, Piece.WHITE)
        piece_four = Piece(Piece.PAWN, Piece.WHITE)
        board = Board(6, 4)
        pieces = [piece_one,piece_two,piece_three,piece_four]
        self.assertTrue(board.add(piece_one, 3, 2))
        self.assertTrue(board.add(piece_two, 4, 1))
        self.assertFalse(board.add(piece_three, 6, 4))
        self.assertFalse(board.add(piece_four, 7, 0))

    """ Formato de salida cambiado para facilitar visualizacion
    def test_print_board(self):
        board = Board(3, 2)
        piece_one = Piece(Piece.PAWN, Piece.BLACK)
        piece_two = Piece(Piece.PAWN, Piece.BLACK)
        piece_three = Piece(Piece.PAWN, Piece.WHITE)
        piece_four = Piece(Piece.PAWN, Piece.WHITE)
        self.assertTrue(board.add(piece_one, 0, 0))
        self.assertTrue(board.add(piece_two, 0, 1))
        self.assertTrue(board.add(piece_three, 2, 0))
        self.assertTrue(board.add(piece_four, 2, 1))
        expectedResult = "Pb Pb \n.  .  \nPw Pw \n"
        self.assertEquals(expectedResult, board.to_string())
    """


    def test_euclidean_distance(self):
        board = Board(6, 4)
        self.assertEquals(board.get_distance_to_enemy_king([1, 2], [3,3]), 5**(1.0/2))
 

    def test_is_legal_movement_pawn(self):
        board = Board(6, 4)
        piece_pawn = Piece(Piece.PAWN, Piece.BLACK)
        piece_pawn_two = Piece(Piece.PAWN, Piece.BLACK)
        piece_king = Piece(Piece.KING, Piece.WHITE)
        piece_white_pawn = Piece(Piece.PAWN, Piece.WHITE)
        board.add(piece_king, 5, 2)
        board.add(piece_pawn, 3, 2)
        board.add(piece_pawn_two, 4, 3)
        board.add(piece_white_pawn, 4, 1)
        available_positions = [[4, 2], [4, 1]]
        self.assertEquals(board.is_legal_movement(3, 2), available_positions);


    def test_is_legal_movement_king(self):
        board = Board(20, 20)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_king_black = Piece(Piece.KING, Piece.BLACK)
        board.add(piece_king_white, 10, 10)
        board.add(piece_king_black, 15, 10)
        available_positions = [[11, 11], [11, 10], [11, 9]]
        self.assertEqual(board.is_legal_movement(10, 10).sort(), available_positions.sort())


    def test_is_legal_movement_rook_right(self):
        board = Board (20, 20)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_rook_black = Piece(Piece.ROOK, Piece.BLACK)    
        board.add(piece_king_white, 15, 13)
        board.add(piece_rook_black, 15, 10)
        available_positions = [[15, 11], [15, 12], [15, 13]]
        self.assertEqual(board.is_legal_movement(15, 10), available_positions)


    def test_is_legal_movement_rook_left(self):
        board = Board (20, 20)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_rook_black = Piece(Piece.ROOK, Piece.BLACK)    
        board.add(piece_king_white, 15, 7)
        board.add(piece_rook_black, 15, 10)
        available_positions = [[15, 9], [15, 8], [15, 7]]
        self.assertEqual(board.is_legal_movement(15, 10), available_positions)


    def test_is_legal_movement_rook_down(self):
        board = Board (20, 20)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_rook_black = Piece(Piece.ROOK, Piece.BLACK)    
        board.add(piece_king_white, 18, 10)
        board.add(piece_rook_black, 15, 10)
        available_positions = [[16, 10], [17, 10], [18, 10]]
        self.assertEqual(board.is_legal_movement(15, 10), available_positions)


    def test_is_legal_movement_rook_up(self):
        board = Board (20, 20)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_rook_black = Piece(Piece.ROOK, Piece.BLACK)    
        board.add(piece_king_white, 12, 10)
        board.add(piece_rook_black, 15, 10)
        available_positions = [[14, 10], [13, 10], [12, 10]]
        self.assertEqual(board.is_legal_movement(15, 10), available_positions)


    def test_another_is_legal_movement_rook_up(self):
        board = Board(6, 6)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_rook_black = Piece(Piece.ROOK, Piece.BLACK)
        piece_pawn_black = Piece(Piece.PAWN, Piece.BLACK) 
        board.add(piece_king_white, 0, 2)
        board.add(piece_rook_black, 3, 3)
        board.add(piece_pawn_black, 3, 2)
        available_positions = [[2, 3], [1, 3], [0, 3]]
        self.assertEqual(board.is_legal_movement(3, 3), available_positions)


    def test_is_legal_movement_rook_all(self):
        board = Board (20, 20)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_rook_black = Piece(Piece.ROOK, Piece.BLACK)   
        piece_pawn_black = Piece(Piece.PAWN, Piece.BLACK)  
        board.add(piece_king_white, 12, 8)
        board.add(piece_rook_black, 18, 10)
        board.add(piece_pawn_black, 17, 10)
        available_positions = [[18, 9], [18, 8], [18, 7]]
        self.assertEqual(board.is_legal_movement(18, 10), available_positions)


    def test_is_legal_movement_bishop_rigth_down(self):
        board = Board (20, 20)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_bishop_black = Piece(Piece.BISHOP, Piece.BLACK)   
        piece_pawn_black = Piece(Piece.PAWN, Piece.BLACK)
        piece_pawn_black_two = Piece(Piece.PAWN, Piece.BLACK)
        piece_pawn_black_three = Piece(Piece.PAWN, Piece.BLACK) 
        board.add(piece_king_white, 19, 12)
        board.add(piece_bishop_black, 18, 10)
        board.add(piece_pawn_black, 17, 9)
        board.add(piece_pawn_black_two, 19 , 9)
        board.add(piece_pawn_black_three, 17 , 11)
        available_positions = [[19, 11]]
        self.assertEqual(board.is_legal_movement(18, 10), available_positions)


    def test_is_legal_movement_bishop_left_down(self):
        board = Board (20, 20)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_bishop_black = Piece(Piece.BISHOP, Piece.BLACK)   
        piece_pawn_black = Piece(Piece.PAWN, Piece.BLACK)
        piece_pawn_black_two = Piece(Piece.PAWN, Piece.BLACK)
        piece_pawn_black_three = Piece(Piece.PAWN, Piece.BLACK) 
        board.add(piece_king_white, 19, 8)
        board.add(piece_bishop_black, 18, 10)
        board.add(piece_pawn_black, 17, 9)
        board.add(piece_pawn_black_two, 16 , 11)
        board.add(piece_pawn_black_three, 17 , 11)
        available_positions = [[19, 9]]
        self.assertEqual(board.is_legal_movement(18, 10), available_positions)


    def test_is_legal_movement_bishop_left_up(self):
        board = Board (20, 20)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_bishop_black = Piece(Piece.BISHOP, Piece.BLACK)   
        piece_pawn_black = Piece(Piece.PAWN, Piece.BLACK)
        piece_pawn_black_two = Piece(Piece.PAWN, Piece.BLACK)
        piece_pawn_black_three = Piece(Piece.PAWN, Piece.BLACK) 
        board.add(piece_king_white, 15, 7)
        board.add(piece_bishop_black, 18, 10)
        board.add(piece_pawn_black, 17, 11)
        board.add(piece_pawn_black_two, 19 , 9)
        board.add(piece_pawn_black_two, 14 , 6)
        available_positions = [[17, 9],[16, 8], [15, 7]]
        self.assertEqual(board.is_legal_movement(18, 10), available_positions)


    def test_is_legal_movement_bishop_rigth_up(self):
        board = Board (20, 20)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_bishop_black = Piece(Piece.BISHOP, Piece.BLACK)   
        piece_pawn_black = Piece(Piece.PAWN, Piece.BLACK)
        piece_pawn_black_two = Piece(Piece.PAWN, Piece.BLACK)
        piece_pawn_black_three = Piece(Piece.PAWN, Piece.BLACK) 
        board.add(piece_king_white, 15, 13)
        board.add(piece_bishop_black, 18, 10)
        board.add(piece_pawn_black, 17, 19)
        board.add(piece_pawn_black_two, 14 , 14)
        available_positions = [[17, 11],[16, 12], [15, 13]]
        self.assertEqual(board.is_legal_movement(18, 10), available_positions)
    

    def test_is_legal_movement_queen(self):
        board = Board(6, 6)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_queen_black = Piece(Piece.QUEEN, Piece.BLACK)
        board.add(piece_king_white, 0, 2)
        board.add(piece_queen_black, 3, 3)
        available_positions = [[3, 2], [2, 3], [1, 3], [0, 3], [2, 2], [1, 1], [0, 0], [2, 4]]
        self.assertEqual(board.is_legal_movement(3, 3), available_positions)


    def test_move_no_pawn(self):
        board = Board(6, 6)
        piece_king_white = Piece(Piece.KING, Piece.WHITE)
        piece_queen_black = Piece(Piece.QUEEN, Piece.BLACK)
        piece_rook_black = Piece(Piece.ROOK, Piece.BLACK)
        board.add(piece_king_white, 0, 2)
        board.add(piece_queen_black, 3, 3)
        board.add(piece_rook_black, 4, 3)
        self.assertTrue(board.move_piece(3,3,0,0))
        self.assertEqual(board.get_piece_in_pos(0,0), piece_queen_black)
        self.assertTrue(board.move_piece(4,3,3,3))
        self.assertEqual(board.get_piece_in_pos(3,3), piece_rook_black)
    

    def test_move_a_pawn(self):
        board = Board(6, 6)
        piece_pawn_black = Piece(Piece.PAWN, Piece.BLACK)
        piece_pawn_white = Piece(Piece.PAWN, Piece.WHITE)
        
        board.add(piece_pawn_black, 3, 3)
        board.add(piece_pawn_white, 4, 3)
        self.assertFalse(board.move_piece(3,3,4,3))
        self.assertEqual(board.get_piece_in_pos(3,3), piece_pawn_black)
        self.assertFalse(board.move_piece(4,3,3,3))
        self.assertEqual(board.get_piece_in_pos(4,3), piece_pawn_white)
       

    def test_is_check(self):
        board = Board(6, 6)
        p_king_white = Piece (Piece.KING, Piece.WHITE)
        board.add(p_king_white, 0, 2)
        p_queen_black = Piece (Piece.QUEEN, Piece.BLACK)
        board.add(p_queen_black, 2, 4)
        self.assertTrue(board.is_check_for_enemy(Piece.WHITE))
    

    def test_is_check_only_two_kings(self):
        board  = Board(4, 4)
        p_king_black = Piece(Piece.KING, Piece.BLACK)
        p_king_white = Piece(Piece.KING, Piece.WHITE)
        board.add(p_king_black, 0, 0)
        board.add(p_king_white, 0, 1)
        self.assertTrue(board.is_check_for_enemy(Piece.WHITE))
        self.assertTrue(board.is_check_for_enemy(Piece.BLACK))


    def test_new_game(self):
        player_one = Player(Player.HUMAN, Piece.WHITE)
        player_two = Player(Player.HUMAN, Piece.BLACK)
        g_game = Game(player_one, player_two)
        self.assertEqual(g_game.get_player_turn(), player_one)
    

    def test_is_check_but_not_terminal(self):
        board  = Board(4, 4)
        p_king_black = Piece(Piece.KING, Piece.BLACK)
        p_king_white = Piece(Piece.KING, Piece.WHITE)
        board.add(p_king_black, 0, 0)
        board.add(p_king_white, 0, 1)
        player_one = Player(Player.HUMAN, Piece.WHITE)
        player_two = Player(Player.HUMAN, Piece.BLACK)
        g_game = Game(player_one, player_two) 
        self.assertFalse(g_game.is_terminal(board))


    def test_change_turns(self):
        board = Board(4, 4)
        player_one = Player(Player.HUMAN, Piece.WHITE)
        player_two = Player(Player.HUMAN, Piece.BLACK)
        g_game = Game(player_one, player_two)
        self.assertEquals(g_game.get_player_turn(), g_game.get_player_one())
        g_game.change_turn()
        self.assertEquals(g_game.get_player_turn(), g_game.get_player_two())
        g_game.change_turn()
        self.assertEquals(g_game.get_player_turn(), g_game.get_player_one())
        g_game.change_turn()
        self.assertEquals(g_game.get_player_turn(), g_game.get_player_two())


    def test_initialize_default_board(self): # Esta correctamente formateado
        board = Board(6, 4)
        board.initialize_default_board()
        self.assertFalse(board.is_empty())
    
        """
    def test_start_game(self):
        player_one = Player(Player.HUMAN, Piece.WHITE)
        player_two = Player(Player.HUMAN, Piece.BLACK)
        g_game = Game(player_one, player_two)
        g_game.start_game() """


    def test_sucessors_for_a_little_board_with_a_few_pieces(self):
        board = Board(3, 2)
        b_king = Piece(Piece.KING, Piece.BLACK)
        b_queen = Piece(Piece.QUEEN, Piece.BLACK)

        w_king = Piece(Piece.KING, Piece.WHITE)
        w_queen = Piece(Piece.QUEEN, Piece.WHITE)

        board.add(b_queen, 0, 0)
        board.add(b_king, 0, 1)
        board.add(w_queen, 2, 1)
        board.add(w_king, 2, 0)

        player_one = Player(Player.IDIOT, Piece.WHITE)
        player_two = Player(Player.HUMAN, Piece.BLACK)
        game = Game(player_one, player_two)
        board_copy = copy.deepcopy(board)
        # print game.successors(board)

        self.assertEqual(board.to_string(), board_copy.to_string())


    def test_sucessors_for_the_default_board(self):
        board = Board(6, 4)
        board.initialize_default_board()

        player_one = Player(Player.IDIOT, Piece.BLACK)
        player_two = Player(Player.IDIOT, Piece.WHITE)
        game = Game(player_one, player_two)

        board_copy = copy.deepcopy(board)

        self.assertEqual(board.to_string(), board_copy.to_string())

    def test_utility_is_inf_white(self):
        board  = Board(4, 4)
        p_king_black = Piece(Piece.KING, Piece.BLACK)
        p_king_white = Piece(Piece.KING, Piece.WHITE)
        board.add(p_king_black, 0, 0)
        board.add(p_king_white, 0, 1)
        player_one = Player(Player.IDIOT, Piece.WHITE)
        player_two = Player(Player.HUMAN, Piece.BLACK)
        g_game = Game(player_one, player_two)
        inf = 99999999
        self.assertEqual(inf, g_game.utility(board, player_one))

    def test_utility_is_inf_black(self):
        board = Board(4, 4)
        p_king_black = Piece(Piece.KING, Piece.BLACK)
        p_king_white = Piece(Piece.KING, Piece.WHITE)
        board.add(p_king_black, 0, 0)
        board.add(p_king_white, 0, 1)
        player_one = Player(Player.IDIOT, Piece.WHITE)
        player_two = Player(Player.IDIOT, Piece.BLACK)
        g_game = Game(player_one, player_two)
        inf = 99999999
        self.assertEqual(inf, g_game.utility(board, player_two))
    
    def test_utility_is_negative_inf_white(self):
        board  = Board(4, 4)
        p_king_black = Piece(Piece.KING, Piece.BLACK)
        p_queen_black = Piece(Piece.QUEEN, Piece.BLACK)
        p_king_white = Piece(Piece.KING, Piece.WHITE)
        board.add(p_king_black, 0, 0)
        board.add(p_queen_black, 2, 0)
        board.add(p_king_white, 0, 2)
        player_one = Player(Player.IDIOT, Piece.WHITE)
        player_two = Player(Player.IDIOT, Piece.BLACK)
        g_game = Game(player_one, player_two)
        inf = -99999999
        self.assertEqual(inf, g_game.utility(board, player_one))


    def test_utility_is_negative_inf_black(self):
        board  = Board(4, 4)
        p_king_black = Piece(Piece.KING, Piece.BLACK)
        p_queen_white = Piece(Piece.QUEEN, Piece.WHITE)
        p_king_white = Piece(Piece.KING, Piece.WHITE)
        board.add(p_king_black, 0, 0)
        board.add(p_queen_white, 2, 2)
        board.add(p_king_white, 0, 2)
        player_one = Player(Player.IDIOT, Piece.WHITE)
        player_two = Player(Player.IDIOT, Piece.BLACK)
        g_game = Game(player_one, player_two)
        inf = -99999999
        self.assertEqual(inf, g_game.utility(board, player_two))

    def test_utility_in_random_board_should_be_zero(self):
        
        board  = Board(4, 4)
        p_king_black = Piece(Piece.KING, Piece.BLACK)
        p_rook_black = Piece(Piece.ROOK, Piece.BLACK)
        p_rook_white = Piece(Piece.ROOK, Piece.WHITE)
        p_king_white = Piece(Piece.KING, Piece.WHITE)
        board.add(p_king_black, 0, 0)
        board.add(p_rook_black, 2, 0)
        board.add(p_rook_white, 1, 1)
        board.add(p_king_white, 0, 2)
        player_one = Player(Player.IDIOT, Piece.WHITE)
        player_two = Player(Player.IDIOT, Piece.BLACK)
        g_game = Game(player_one, player_two)
        self.assertEqual(0, g_game.utility(board, player_one))

        
    def test_get_enemy_king_white_turn(self):
        board = Board(4, 4)
        p_king_black = Piece(Piece.KING, Piece.BLACK)
        board.add(p_king_black, 0, 0)
        self.assertEqual(board.get_enemy_king(Piece.WHITE), [0, 0])

    def test_get_enemy_king_black_turn(self):
        board = Board(4, 4)
        p_king_black = Piece(Piece.KING, Piece.WHITE)
        board.add(p_king_black, 0, 0)
        self.assertEqual(board.get_enemy_king(Piece.BLACK), [0, 0])

    def test_can_kill_default_special_board_player_black(self):
        board = Board(6, 4)
        board.initialize_default_board()
        self.assertFalse(board.can_kill(Piece.BLACK))
        self.assertFalse(board.can_be_killed(Piece.WHITE))
        self.assertFalse(board.can_be_killed(Piece.BLACK))
        self.assertFalse(board.can_kill(Piece.WHITE))

    def test_save_a_default_game(self):
        board = Board(6, 4)
        board.initialize_default_board()
        player_one = Player(Player.IDIOT, Piece.WHITE)
        player_two = Player(Player.IDIOT, Piece.BLACK)
        g_game = Game(player_one, player_two)

        g_game.save(board)





if __name__ == '__main__':
    unittest.main()
