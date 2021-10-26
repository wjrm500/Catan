from actions.Action import Action
import json

class AddPlayer(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.players = data['players']