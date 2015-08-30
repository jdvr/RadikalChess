class Piece(object):
    
    PAWN = 'P'
    KING = 'K'
    ROOK = 'R'
    BISHOP = 'B'
    QUEEN = 'Q'

    VALUES = {
              'P' : 1,
              'R' : 8,
              'B' : 10,
              'Q' : 25,
              'K' : 50
              }
    
    BLACK = 'b'
    WHITE = 'w'

    def __init__(self, type_piece, color):
        self.__type = type_piece
        self.__color = color

       
    def to_string(self):
        return self.__type + self.__color


    def get_color(self):
        return self.__color


    def get_type(self):
        return self.__type

        
