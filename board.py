from piece import Piece
import time


class Board(object):
    """description of class"""

    def __init__(self, rows, columns):
        self.__board = [[None for col in range(columns)] for row in range(rows)] # esto tiene que se optmizable
        self.__rows = rows
        self.__columns = columns
        self.__states = dict()
        self.__n_states = 0

    def get_states(self):
        return self.__states

    def get_board(self):
        return self.__board

    def is_empty(self):
        for row in self.__board:
            for pos in row:
                if pos is not None:
                    return False
        return True

    def add(self, piece, row, col):
        try:
            self.__board[row][col] = piece
            return True
        except IndexError:
            return False

    def to_string(self):
        res = ""
        i = 0
        for row in self.__board:
            res += str(i) + " "
            for pos in row:
                if pos is None:
                    res += ".  "
                else:
                    res += pos.to_string() + " "
            res += "\n"
            i += 1
        i = 0
        for x in self.__board[0]:
            res += "  " + str(i)
            i += 1
        res += "\n"
        return res

    def move_piece(self, o_row, o_column, d_row, d_column):
        if [d_row, d_column] in self.is_legal_movement(o_row, o_column):
            self.__board[d_row][d_column] = self.__board[o_row][o_column]
            self.__board[o_row][o_column] = None
            if self.get_piece_in_pos(d_row, d_column).get_type() is Piece.PAWN:
                if d_row is 0 and self.get_piece_in_pos(d_row, d_column).get_color() is Piece.WHITE:
                    self.__board[d_row][d_column] = Piece(Piece.QUEEN, Piece.WHITE)
                if d_row is len(self.__board) - 1 and self.get_piece_in_pos(d_row, d_column).get_color() is Piece.BLACK:
                    self.__board[d_row][d_column] = Piece(Piece.QUEEN, Piece.BLACK)
            self.__states[self.__n_states] = self.to_json()
            self.__n_states += 1
            return True
        else:
            return False

    def get_piece_in_pos(self, row, column):
        return self.__board[row][column]

    def get_pos_of_piece(self, piece):
        for x in range(self.__rows):
            for y in range(self.__columns):
                if self.__board[x][y] == piece:
                    return [x, y]

    def get_enemy_king(self, color):
        """ Devuelve el rey del color contrario al pasado por parametro """
        for x in range(self.__rows):
            for y in range(self.__columns):
                if self.__board[x][y] is not None:
                    if self.__board[x][y].get_color() is not color:
                        if self.__board[x][y].get_type() is Piece.KING:
                            return [x, y]

    @staticmethod
    def get_distance_to_enemy_king(piece_pos, enemy_king_pos):
        a = (piece_pos[0] - enemy_king_pos[0]) ** 2
        b = (piece_pos[1] - enemy_king_pos[1]) ** 2
        return (a + b) ** (1.0 / 2)

    def is_a_correct_pos(self, pos):
        if pos[0] < 0 or pos[0] >= len(self.__board):
            return False
        if pos[1] < 0 or pos[1] >= len(self.__board[0]):
            return False
        return True

    def is_legal_movement_pawn(self, row, column, piece):
        available_positions = []
        if piece.get_color() is Piece.WHITE:
            available_positions.append([row - 1, column])
            available_positions.append([row - 1, column - 1])
            available_positions.append([row - 1, column + 1])
        else:
            available_positions.append([row + 1, column])
            available_positions.append([row + 1, column - 1])
            available_positions.append([row + 1, column + 1])

        available_copy = [pos for pos in available_positions]

        for pos in available_copy:
            if self.is_a_correct_pos(pos):
                if self.__board[pos[0]][pos[1]] is not None:
                    if self.get_piece_in_pos(pos[0], pos[1]).get_color() is piece.get_color():
                        available_positions.remove(pos)
                    elif pos[1] is column:
                        available_positions.remove(pos)
                if self.__board[pos[0]][pos[1]] is None:
                    if pos[1] is column - 1:
                        available_positions.remove(pos)
                    elif pos[1] is column + 1:
                        available_positions.remove(pos)
            else:
                available_positions.remove(pos)
        return available_positions

    def is_legal_movement_king(self, row, column, piece, enemy_king):
        available_positions = []
        for x, y in [(row + i, column + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if
                     i != 0 or j != 0]:
            if self.is_a_correct_pos([x, y]):
                if self.__board[x][y] is None:
                    available_positions.append([x, y])
                elif self.get_piece_in_pos(x, y).get_color() is not piece.get_color():
                    available_positions.append([x, y])

        original_distance = self.get_distance_to_enemy_king(self.get_pos_of_piece(piece), enemy_king)
        return [pos for pos in available_positions if
                self.get_distance_to_enemy_king(pos, enemy_king) < original_distance or self.__board[pos[0]][
                    pos[1]] is not None]

    def is_legal_movement_rook(self, row, column, piece, enemy_king):
        available_positions = []
        for x in range(column, len(self.__board[0]), 1):
            if self.__board[row][x] is None:
                available_positions.append([row, x])
            elif self.__board[row][x] is piece:
                continue
            elif self.__board[row][x].get_color() is piece.get_color():
                break
            elif self.__board[row][x].get_color() is not piece.get_color():
                available_positions.append([row, x])
                break

        for x in range(column, -1, -1):
            if self.__board[row][x] is None:
                available_positions.append([row, x])
            elif self.__board[row][x] is piece:
                continue
            elif self.__board[row][x].get_color() is piece.get_color():
                break
            elif self.__board[row][x].get_color() is not piece.get_color():
                available_positions.append([row, x])
                break

        for x in range(row, len(self.__board), 1):
            if self.__board[x][column] is None:
                available_positions.append([x, column])
            elif self.__board[x][column] is piece:
                continue
            elif self.__board[x][column].get_color() is piece.get_color():
                break
            elif self.__board[x][column].get_color() is not piece.get_color():
                available_positions.append([x, column])
                break

        for x in range(row, -1, -1):
            if self.__board[x][column] is None:
                available_positions.append([x, column])
            elif self.__board[x][column] is piece:
                continue
            elif self.__board[x][column].get_color() is piece.get_color():
                break
            elif self.__board[x][column].get_color() is not piece.get_color():
                available_positions.append([x, column])
                break

        original_distance = self.get_distance_to_enemy_king(self.get_pos_of_piece(piece), enemy_king)
        return [pos for pos in available_positions if
                self.get_distance_to_enemy_king(pos, enemy_king) < original_distance or self.__board[pos[0]][
                    pos[1]] is not None]

    def is_legal_movement_bishop(self, row, column, piece, enemy_king):
        available_positions = []
        for x in range(1, len(self.__board), 1):
            if self.is_a_correct_pos([row + x, column + x]):
                if self.__board[row + x][column + x] is None:
                    available_positions.append([row + x, column + x])
                elif self.__board[row + x][column + x].get_color() is piece.get_color():
                    break
                elif self.__board[row + x][column + x].get_color() is not piece.get_color():
                    available_positions.append([row + x, column + x])
                    break

        for y in range(1, len(self.__board), 1):
            if self.is_a_correct_pos([row + y, column - y]):
                if self.__board[row + y][column - y] is None:
                    available_positions.append([row + y, column - y])
                elif self.__board[row + y][column - y].get_color() is piece.get_color():
                    break
                elif self.__board[row + y][column - y].get_color() is not piece.get_color():
                    available_positions.append([row + y, column - y])
                    break

        for z in range(1, len(self.__board), +1):
            if self.is_a_correct_pos([row - z, column - z]):
                if self.__board[row - z][column - z] is None:
                    available_positions.append([row - z, column - z])
                elif self.__board[row - z][column - z].get_color() is piece.get_color():
                    break
                elif self.__board[row - z][column - z].get_color() is not piece.get_color():
                    available_positions.append([row - z, column - z])
                    break

        for h in range(1, len(self.__board), +1):
            if self.is_a_correct_pos([row - h, column + h]):
                if self.__board[row - h][column + h] is None:
                    available_positions.append([row - h, column + h])
                elif self.__board[row - h][column + h].get_color() is piece.get_color():
                    break
                elif self.__board[row - h][column + h].get_color() is not piece.get_color():
                    available_positions.append([row - h, column + h])
                    break

        original_distance = self.get_distance_to_enemy_king(self.get_pos_of_piece(piece), enemy_king)
        return [pos for pos in available_positions if
                self.get_distance_to_enemy_king(pos, enemy_king) < original_distance or self.__board[pos[0]][
                    pos[1]] is not None]

    def is_legal_movement_queen(self, row, column, piece, enemy_king):
        available_positions = self.is_legal_movement_rook(row, column, piece, enemy_king)
        bishop_positions = self.is_legal_movement_bishop(row, column, piece, enemy_king)
        for diagonal_pos in bishop_positions:
            available_positions.append(diagonal_pos)

        return available_positions

    def is_legal_movement(self, row, column):
        piece = self.get_piece_in_pos(row, column)
        enemy_king = self.get_enemy_king(piece.get_color())  # = array de 2 pos [x, y]
        if enemy_king is None and piece.get_type() is not Piece.PAWN:
            return None
        ### PAWN MOVEMENTS ###
        if piece.get_type() is Piece.PAWN:
            return self.is_legal_movement_pawn(row, column, piece)

        ### KING MOVEMENTS ###
        elif piece.get_type() is Piece.KING:
            return self.is_legal_movement_king(row, column, piece, enemy_king)

        ### ROOK MOVEMENTS ### 
        elif piece.get_type() is Piece.ROOK:
            return self.is_legal_movement_rook(row, column, piece, enemy_king)

        ### BISHOP MOVEMENTS ###
        elif piece.get_type() is Piece.BISHOP:
            return self.is_legal_movement_bishop(row, column, piece, enemy_king)

        ### QUEEN MOVEMENTS ###
        elif piece.get_type() is Piece.QUEEN:
            return self.is_legal_movement_queen(row, column, piece, enemy_king)

    def is_check_for_enemy(self, this_turn_color):
        """Returns true if it's check, false otherwise"""

        if this_turn_color is Piece.WHITE:
            my_king = self.get_enemy_king(Piece.BLACK)
            enemy_king = self.get_enemy_king(Piece.WHITE)
        else:
            my_king = self.get_enemy_king(Piece.WHITE)
            enemy_king = self.get_enemy_king(Piece.BLACK)
        if my_king is None or enemy_king is None:
            return True

        for x in range(0, len(self.__board), 1):
            for y in range(0, len(self.__board[0]), 1):
                if self.__board[x][y] is not None and self.__board[x][y].get_color() is not this_turn_color:
                    if my_king in self.is_legal_movement(x, y):
                        return True
        return False

    def is_check_mate_for_enemy(self, this_turn_color):
        if this_turn_color is Piece.WHITE:
            my_king = self.get_enemy_king(Piece.BLACK)
        else:
            my_king = self.get_enemy_king(Piece.WHITE)
        if my_king is None:
            return True

        for x in range(self.__rows):
            for y in range(self.__columns):
                if self.__board[x][y] is not None and self.__board[x][y].get_color() is not this_turn_color:
                    if my_king in self.is_legal_movement(x, y):
                        return True

        return False

    def initialize_player_defined_board(self):
        pass

    def initialize_black_one_move_win(self):

        b_pawn_one = Piece(Piece.PAWN, Piece.BLACK)
        b_pawn_two = Piece(Piece.PAWN, Piece.BLACK)
        b_pawn_three = Piece(Piece.PAWN, Piece.BLACK)


        b_king = Piece(Piece.KING, Piece.BLACK)
        b_queen = Piece(Piece.QUEEN, Piece.BLACK)
        b_rook = Piece(Piece.ROOK, Piece.BLACK)
        b_bishop = Piece(Piece.BISHOP, Piece.BLACK)

        w_pawn_two = Piece(Piece.PAWN, Piece.WHITE)
        w_pawn_three = Piece(Piece.PAWN, Piece.WHITE)
        w_pawn_four = Piece(Piece.PAWN, Piece.WHITE)

        w_king = Piece(Piece.KING, Piece.WHITE)
        w_queen = Piece(Piece.QUEEN, Piece.WHITE)
        w_rook = Piece(Piece.ROOK, Piece.WHITE)
        w_bishop = Piece(Piece.BISHOP, Piece.WHITE)

        self.add(b_pawn_one, 1, 0)
        self.add(b_pawn_two, 1, 1)
        self.add(b_pawn_three, 1, 2)

        self.add(b_king, 0, 0)
        self.add(b_queen, 0, 1)
        self.add(b_bishop, 0, 2)
        self.add(b_rook, 0, 3)

        self.add(w_pawn_two, 4, 2)
        self.add(w_pawn_three, 4, 1)
        self.add(w_pawn_four, 4, 0)

        self.add(w_king, 5, 3)
        self.add(w_queen, 5, 2)
        self.add(w_rook, 5, 0)
        self.add(w_bishop, 5, 1)

    def initialize_king_and_rook(self):

        b_king = Piece(Piece.KING, Piece.BLACK)
        b_rook = Piece(Piece.ROOK, Piece.BLACK)

        w_king = Piece(Piece.KING, Piece.WHITE)
        w_rook = Piece(Piece.ROOK, Piece.WHITE)

        self.add(b_king, 2, 2)
        self.add(b_rook, 2, 3)

        self.add(w_king, 5, 2)
        self.add(w_rook, 1, 1)

    def initialize_default_board(self):

        b_pawn_one = Piece(Piece.PAWN, Piece.BLACK)
        b_pawn_two = Piece(Piece.PAWN, Piece.BLACK)
        b_pawn_three = Piece(Piece.PAWN, Piece.BLACK)
        b_pawn_four = Piece(Piece.PAWN, Piece.BLACK)

        b_king = Piece(Piece.KING, Piece.BLACK)
        b_queen = Piece(Piece.QUEEN, Piece.BLACK)
        b_rook = Piece(Piece.ROOK, Piece.BLACK)
        b_bishop = Piece(Piece.BISHOP, Piece.BLACK)

        w_pawn_one = Piece(Piece.PAWN, Piece.WHITE)
        w_pawn_two = Piece(Piece.PAWN, Piece.WHITE)
        w_pawn_three = Piece(Piece.PAWN, Piece.WHITE)
        w_pawn_four = Piece(Piece.PAWN, Piece.WHITE)

        w_king = Piece(Piece.KING, Piece.WHITE)
        w_queen = Piece(Piece.QUEEN, Piece.WHITE)
        w_rook = Piece(Piece.ROOK, Piece.WHITE)
        w_bishop = Piece(Piece.BISHOP, Piece.WHITE)

        self.add(b_pawn_one, 1, 0)
        self.add(b_pawn_two, 1, 1)
        self.add(b_pawn_three, 1, 2)
        self.add(b_pawn_four, 1, 3)

        self.add(b_king, 0, 0)
        self.add(b_queen, 0, 1)
        self.add(b_bishop, 0, 2)
        self.add(b_rook, 0, 3)


        self.add(w_pawn_one, 4, 3)
        self.add(w_pawn_two, 4, 2)
        self.add(w_pawn_three, 4, 1)
        self.add(w_pawn_four, 4, 0)

        self.add(w_king, 5, 3)
        self.add(w_queen, 5, 2)
        self.add(w_rook, 5, 0)
        self.add(w_bishop, 5, 1)

    def can_kill(self, player_color):
        for x in range(0, len(self.__board), 1):
            for y in range(0, len(self.__board[0]), 1):
                if self.__board[x][y] is not None and self.__board[x][y].get_color() is player_color:
                    for pos in self.is_legal_movement(x, y):
                        if self.get_piece_in_pos(pos[0], pos[1]) is not None:
                            return True
        return False

    def can_be_killed(self, player_color):
        for x in range(0, len(self.__board), 1):
            for y in range(0, len(self.__board[0]), 1):
                if self.__board[x][y] is not None and self.__board[x][y].get_color() is not player_color:
                    for pos in self.is_legal_movement(x, y):
                        if self.get_piece_in_pos(pos[0], pos[1]) is not None:
                            return True
        return False

    def to_json(self):
        """
         This return a json string which represent the board on a determinate state
        """
        current_board = dict()
        current_board['row'] = self.__rows
        current_board['columns'] = self.__columns
        current_board['board'] = [c for c in self.to_string() if c != "\n" and not c.isdigit() and c != " "]
        return current_board




