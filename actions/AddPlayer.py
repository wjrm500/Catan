from actions.Action import Action

class AddPlayer(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.players = data['players']