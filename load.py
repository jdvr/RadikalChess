import json


class Load:

    def __init__(self):
        f = open('db.games', 'r')
        self.__db_content = f.readlines()
        f.close()

    @staticmethod
    def load_from_file(name):
        f = open(name, 'r')
        saved_board = json.loads(f.readline())
        f.close()
        return saved_board

    def load_db(self):
        return [
            game for game in self.__db_content
        ]

    def compare_with_data_base_states(self, state, player):
        state_json = state.to_json()
        for games in self.__db_content:
            currnt_game = json.loads(games)
            if currnt_game['winner']['color'] == player.get_color():
                db_states = currnt_game['state']
                state = 0
                while True:
                    try:
                        if state_json == db_states[str(state)]:
                            return 20000
                        else:
                            state += 1
                    except KeyError:
                        break
        return 0