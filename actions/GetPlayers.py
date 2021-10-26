from actions.Action import Action
import json

class GetPlayers(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, param):
        chaperone.players = json.loads(param)