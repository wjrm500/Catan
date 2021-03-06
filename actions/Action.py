from frontend.GeneralUtils import GeneralUtils as gutils

class Action:
    def __init__(self):
        pass

    def is_instigating_client(self):
        return self.data['player'].id == self.chaperone.player.id

    def reload_active_player(self):
        ### Update active player client side (to reflect paid for action)
        if self.chaperone.player.id == self.data['player'].id:
            self.chaperone.player.__dict__ = self.data['player'].__dict__

    def reload_all_players(self):
        ### Update all players client side at settling / main game transition (to reflect settlements and roads spent in settling phase)
        for player in self.data['players']:
            if self.chaperone.player.id == player.id:
                self.chaperone.player.__dict__ = player.__dict__

    def refresh_play_frame_handler(self):
        play_frame_handler = self.game_phase.notebook_frame_handlers['play']
        play_frame_handler.update_resource_cards()
        play_frame_handler.update_development_cards()
        play_frame_handler.update_movable_pieces()
        if self.is_instigating_client():
            action_tree_handler = play_frame_handler.action_tree_handler
            action_tree_handler.cancel(event = None)
            action_tree_handler.fill_action_tree()
    
    def refresh_game_board(self, full_refresh = False):
        if self.is_instigating_client():
            self.game_phase.hexagon_rendering.handle_leave(event = None, full_refresh = full_refresh)
        else:
            if full_refresh:
                self.game_phase.hexagon_rendering.draw_board()
            self.game_phase.hexagon_rendering.draw_board_items()
        
    def get_history_text_area(self, in_settling_phase):
        return self.game_phase.text_area if in_settling_phase else self.game_phase.notebook_frame_handlers['history'].text_area
    
    def get_chat_text_area(self):
        return self.game_phase.notebook_frame_handlers['chat'].text_area
        
    def enable_text_area(self, text_area):
        text_area.config(state = 'normal')
    
    def disable_text_area(self, text_area):
        text_area.yview('end')
        text_area.config(state = 'disabled')
    
    def text_insert(self, text_area, text, style = None):
        self.enable_text_area(text_area)
        text_area.insert('end', text, style)
        self.disable_text_area(text_area)
        if not gutils.safe_isinstance(self.game_phase, 'SettlingPhase') and text_area is self.game_phase.notebook_frame_handlers['history'].text_area:
            fg_color = 'black'
            if style and any(color in style for color in ['green', 'purple', 'red']):
                fg_color = style.split('_')[0]
            self.game_phase.notification_text.configure({'foreground': fg_color})
            self.game_phase.notification_text_variable.set('Latest action: ' + text.lstrip('\n'))
    
    def refresh_status_frame_handler(self):
        status_frame_handler = self.game_phase.notebook_frame_handlers['status']
        status_frame_handler.load_text_variables()
        status_frame_handler.update_resource_potential_table_frame()