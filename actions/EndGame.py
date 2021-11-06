from actions.Action import Action
import os

class EndGame(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.root.destroy()
        os._exit(0)