from actions.Action import Action

class CreateNewGame(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.game_code = data['game_code']