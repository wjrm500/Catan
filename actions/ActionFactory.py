from actions.AddPlayer import AddPlayer
from actions.BuildRoad import BuildRoad
from actions.BuildVillage import BuildVillage
from actions.BuyDevelopmentCard import BuyDevelopmentCard
from actions.CreateNewGame import CreateNewGame
from actions.EndGame import EndGame
from actions.EndTurn import EndTurn
from actions.JoinExistingGame import JoinExistingGame
from actions.MoveRobberToDesert import MoveRobberToDesert
from actions.PlaceRobber import PlaceRobber
from actions.PlayMonopolyCard import PlayMonopolyCard
from actions.PlayYearOfPlentyCard import PlayYearOfPlentyCard
from actions.RemovePlayer import RemovePlayer
from actions.RollDice import RollDice
from actions.SendChatMessage import SendChatMessage
from actions.StartGame import StartGame
from actions.StartGameProper import StartGameProper
from actions.SwapCards import SwapCards
from actions.TradeWithBank import TradeWithBank
from actions.UpgradeSettlement import UpgradeSettlement

class ActionFactory:
    ADD_PLAYER = 'ADD_PLAYER'
    BUILD_ROAD = 'BUILD_ROAD'
    BUILD_VILLAGE = 'BUILD_VILLAGE'
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
    TRADE_WITH_BANK = 'TRADE_WITH_BANK'
    SWAP_CARDS = 'SWAP_CARDS'
    MOVE_ROBBER_TO_DESERT = 'MOVE_ROBBER_TO_DESERT'

    PLAY_MONOPOLY_CARD = 'PLAY_MONOPOLY_CARD'
    PLAY_YEAR_OF_PLENTY_CARD = 'PLAY_YEAR_OF_PLENTY_CARD'

    SEND_CHAT_MESSAGE = 'SEND_CHAT_MESSAGE'

    @classmethod
    def get_action(cls, action):
        if action == cls.ADD_PLAYER:
            return AddPlayer()
        elif action == cls.BUILD_ROAD:
            return BuildRoad()
        elif action == cls.BUILD_VILLAGE:
            return BuildVillage()
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
        elif action == cls.TRADE_WITH_BANK:
            return TradeWithBank()
        elif action == cls.SWAP_CARDS:
            return SwapCards()
        elif action == cls.MOVE_ROBBER_TO_DESERT:
            return MoveRobberToDesert()
        elif action == cls.PLAY_MONOPOLY_CARD:
            return PlayMonopolyCard()
        elif action == cls.PLAY_YEAR_OF_PLENTY_CARD:
            return PlayYearOfPlentyCard()
        elif action == cls.SEND_CHAT_MESSAGE:
            return SendChatMessage()