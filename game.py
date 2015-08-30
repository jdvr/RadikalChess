from player import Player
from piece import Piece
import copy
from save import Save
from load import Load


class Game(object):
    """This class represent a match with two players"""

    def __init__(self, player_one, player_two):
        self.__player_one = player_one
        self.__player_two = player_two
        self.__player_turn = player_one

    @staticmethod
    def is_terminal(state):
        n_kings = 0
        for row in state.get_board():
            for piece in row:
                if piece is not None and piece.get_type() is Piece.KING:
                    n_kings += 1
                    if n_kings == 2:
                        return False
        return True
        #refactor 2 kings
        

    def get_player_turn(self):
        return self.__player_turn


    def change_turn(self):
        if self.__player_turn is self.__player_one:
            self.__player_turn = self.__player_two
        else:
            self.__player_turn = self.__player_one


    def get_player_one(self):
        return self.__player_one


    def get_player_two(self):
        return self.__player_two

    def get_enemy_player(self):
        if self.__player_turn is self.__player_one:
            return self.__player_two
        else:
            return self.__player_one

    def utility(self, state, player):
        """ This return a value between -infinity and infinity based on how good is the state for the player"""

        player_type = player.get_type()
        player_color = player.get_color()

        if player_color is Piece.WHITE:
            if state.is_check_for_enemy(Piece.BLACK):
                if state.is_check_mate_for_enemy(Piece.BLACK):
                    return 99999999
                else:
                    return 99999999 - 100000
            if state.is_check_for_enemy(Piece.WHITE):
                if state.is_check_mate_for_enemy(Piece.WHITE):
                    return -99999999
                else:
                    return -99999999 + 100000
        elif player_color is Piece.BLACK:
            if state.is_check_for_enemy(Piece.WHITE):
                if state.is_check_mate_for_enemy(Piece.WHITE):
                    return 99999999
                else:
                    return 99999999 - 100000
            if state.is_check_for_enemy(Piece.BLACK):
                if state.is_check_mate_for_enemy(Piece.BLACK):
                    return -99999999
                else:
                    return -99999999 + 100000

        if player_type is Player.IDIOT:
            return 0

        elif player_type is Player.FIGHTER:

            if state.can_kill(player_color):
                state_quality = 50000
            else:
                state_quality = 0

            for row in state.get_board():
                for pos in row:
                    if pos is not None:
                        if pos.get_color() is player_color:
                            state_quality += Piece.VALUES[pos.get_type()]
                        else:
                            state_quality -= Piece.VALUES[pos.get_type()]
            return state_quality

        elif player_type is Player.SMARTEST or player_type is Player.HUMAN:
            db_access = Load()
            can_kill = state.can_kill(player_color)
            can_be_killed = state.can_be_killed(player_color)

            if db_access.compare_with_data_base_states(state, player):
                state_quality = 20000
            else:
                state_quality = 0

            if can_kill and not can_be_killed:
                state_quality += 15000
            elif not can_kill and not can_be_killed:
                state_quality += 10000
            elif can_kill and can_be_killed:
                state_quality -= 5000
            elif not can_kill and can_be_killed:
                state_quality -= 5000

            for row in state.get_board():
                for pos in row:
                    if pos is not None:
                        if pos.get_color() is player_color:
                            state_quality += Piece.VALUES[pos.get_type()]
                        else:
                            state_quality -= Piece.VALUES[pos.get_type()]
            return state_quality

    def successors(self, state, player):
        """Return a list of legal (move, state) pairs."""
        result = []
        for row in state.get_board():
            for piece in row:
                if piece is not None and piece.get_color() is player.get_color():
                    o_pos = state.get_pos_of_piece(piece)
                    available_pos = state.is_legal_movement(o_pos[0],o_pos[1])
                    if available_pos is None:
                        continue
                    for d_pos in available_pos:
                        my_state = copy.deepcopy(state)
                        my_state.move_piece(o_pos[0], o_pos[1], d_pos[0], d_pos[1])
                        result.append([[o_pos, d_pos], my_state])
        return result

    def save(self, state):
        save_game = Save(self.__hash__())
        save_game.add_players(self.__player_one, self.__player_two)
        save_game.add_board(state.to_json())
        save_game.dump_to(Save.FILE)

    def to_db(self, state, winner):
        add_game_to_db = Save(self.__hash__())
        add_game_to_db.add_players(self.__player_one, self.__player_two)
        add_game_to_db.add_board(state.get_states())
        add_game_to_db.add_winner(winner)
        add_game_to_db.dump_to(Save.DATA_BASE)

    @staticmethod
    def load(save_game):
        player_one = Player(save_game['playerone']['type'], save_game['playerone']['color'])
        player_two = Player(save_game['playertwo']['type'], save_game['playertwo']['color'])
        return Game(player_one, player_two)