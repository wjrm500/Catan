from actions.Action import Action

class JoinExistingGame(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, param):
        chaperone.game_code = param