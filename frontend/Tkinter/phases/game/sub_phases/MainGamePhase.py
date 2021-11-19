from frontend.Tkinter.phases.game.GamePhase import GamePhase

class MainGamePhase(GamePhase):
    def update_active_player_index(self):
        self.active_player_index += 1
        if self.active_player_index > len(self.players) - 1:
            self.active_player_index = 0