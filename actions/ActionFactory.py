from actions.AddPlayer import AddPlayer
from actions.CreateNewGame import CreateNewGame
from actions.JoinExistingGame import JoinExistingGame
from actions.StartGame import StartGame

class ActionFactory:
    ADD_PLAYER = 'ADD_PLAYER'
    CREATE_NEW_GAME = 'CREATE_NEW_GAME'
    JOIN_EXISTING_GAME = 'JOIN_EXISTING_GAME'
    START_GAME = 'START_GAME'

    @classmethod
    def get_action(cls, action):
        if action == cls.ADD_PLAYER:
            return AddPlayer()
        elif action == cls.CREATE_NEW_GAME:
            return CreateNewGame()
        elif action == cls.JOIN_EXISTING_GAME:
            return JoinExistingGame()
        elif action == cls.START_GAME:
            return StartGame()