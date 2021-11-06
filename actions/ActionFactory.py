from actions.AddPlayer import AddPlayer
from actions.CreateNewGame import CreateNewGame
from actions.EndGame import EndGame
from actions.JoinExistingGame import JoinExistingGame
from actions.RemovePlayer import RemovePlayer
from actions.StartGame import StartGame

class ActionFactory:
    ADD_PLAYER = 'ADD_PLAYER'
    CREATE_NEW_GAME = 'CREATE_NEW_GAME'
    END_GAME = 'END_GAME'
    JOIN_EXISTING_GAME = 'JOIN_EXISTING_GAME'
    REMOVE_PLAYER = 'REMOVE_PLAYER'
    START_GAME = 'START_GAME'

    @classmethod
    def get_action(cls, action):
        if action == cls.ADD_PLAYER:
            return AddPlayer()
        elif action == cls.CREATE_NEW_GAME:
            return CreateNewGame()
        elif action == cls.END_GAME:
            return EndGame()
        elif action == cls.JOIN_EXISTING_GAME:
            return JoinExistingGame()
        elif action == cls.REMOVE_PLAYER:
            return RemovePlayer()
        elif action == cls.START_GAME:
            return StartGame()