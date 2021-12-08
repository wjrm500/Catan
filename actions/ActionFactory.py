from actions.AddPlayer import AddPlayer
from actions.BuildRoad import BuildRoad
from actions.BuildSettlement import BuildSettlement
from actions.BuyDevelopmentCard import BuyDevelopmentCard
from actions.CreateNewGame import CreateNewGame
from actions.EndGame import EndGame
from actions.EndTurn import EndTurn
from actions.JoinExistingGame import JoinExistingGame
from actions.PlaceRobber import PlaceRobber
from actions.RemovePlayer import RemovePlayer
from actions.RollDice import RollDice
from actions.StartGame import StartGame
from actions.StartGameProper import StartGameProper
from actions.TradeWithBank import TradeWithBank
from actions.main_game.MoveRobberToDesert import MoveRobberToDesert
from actions.main_game.SwapCards import SwapCards
from actions.main_game.UpgradeSettlement import UpgradeSettlement
from actions.main_game.UseDevelopmentCard import UseDevelopmentCard

class ActionFactory:
    ADD_PLAYER = 'ADD_PLAYER'
    BUILD_ROAD = 'BUILD_ROAD'
    BUILD_SETTLEMENT = 'BUILD_SETTLEMENT'
    CREATE_NEW_GAME = 'CREATE_NEW_GAME'
    END_GAME = 'END_GAME'
    JOIN_EXISTING_GAME = 'JOIN_EXISTING_GAME'
    REMOVE_PLAYER = 'REMOVE_PLAYER'
    START_GAME = 'START_GAME'
    START_GAME_PROPER = 'START_GAME_PROPER'

    ### Main game-specific actions
    ROLL_DICE = 'ROLL_DICE'
    END_TURN = 'END_TURN'
    PLACE_ROBBER = 'PLACE_ROBBER'

    UPGRADE_SETTLEMENT = 'UPGRADE_SETTLEMENT'
    BUY_DEVELOPMENT_CARD = 'BUY_DEVELOPMENT_CARD'
    USE_DEVELOPMENT_CARD = 'USE_DEVELOPMENT_CARD'
    TRADE_WITH_BANK = 'TRADE_WITH_BANK'
    SWAP_CARDS = 'SWAP_CARDS'
    MOVE_ROBBER_TO_DESERT = 'MOVE_ROBBER_TO_DESERT'

    @classmethod
    def get_action(cls, action):
        if action == cls.ADD_PLAYER:
            return AddPlayer()
        elif action == cls.BUILD_ROAD:
            return BuildRoad()
        elif action == cls.BUILD_SETTLEMENT:
            return BuildSettlement()
        elif action == cls.CREATE_NEW_GAME:
            return CreateNewGame()
        elif action == cls.END_GAME:
            return EndGame()
        elif action == cls.JOIN_EXISTING_GAME:
            return JoinExistingGame()
        elif action == cls.REMOVE_PLAYER:
            return RemovePlayer()
        elif action == cls.ROLL_DICE:
            return RollDice()
        elif action == cls.END_TURN:
            return EndTurn()
        elif action == cls.PLACE_ROBBER:
            return PlaceRobber()
        elif action == cls.START_GAME:
            return StartGame()
        elif action == cls.START_GAME_PROPER:
            return StartGameProper()
        elif action == cls.UPGRADE_SETTLEMENT:
            return UpgradeSettlement()
        elif action == cls.BUY_DEVELOPMENT_CARD:
            return BuyDevelopmentCard()
        elif action == cls.USE_DEVELOPMENT_CARD:
            return UseDevelopmentCard()
        elif action == cls.TRADE_WITH_BANK:
            return TradeWithBank()
        elif action == cls.SWAP_CARDS:
            return SwapCards()
        elif action == cls.MOVE_ROBBER_TO_DESERT:
            return MoveRobberToDesert()