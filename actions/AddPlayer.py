from actions.Action import Action

class AddPlayer(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.players.append(data['player'])
        if isinstance(chaperone.player, str): ### If the receiving client was also the sending client
            chaperone.player = data['player']