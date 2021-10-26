from actions.Action import Action

class JoinExistingGame(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.game_code = data['game_code']
        chaperone.players = data['players']