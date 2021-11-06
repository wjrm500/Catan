from actions.Action import Action

class RemovePlayer(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.players.remove(data['player'])