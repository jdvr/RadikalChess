from piece import Piece


class Player(object):   
    
    HUMAN = "human_player"
    RANDOM = "random_bot"
    IDIOT = "idiot_bot"
    FIGHTER = "fighter_bot"
    SMARTEST = "smart_and_slow_bot"

    def __init__(self, player_type, player_color):
        self.__type = player_type
        self.__color = player_color

    def get_type(self):
        return self.__type

    def get_color(self):
        return self.__color

    def to_string(self):
        return " Player Type "+ self.__type + " Player Color "+ self.__color

    def to_json(self):
        return {
            'type':   self.__type,
            'color':   self.__color
        }

    


