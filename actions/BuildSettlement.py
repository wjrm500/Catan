import functools

from actions.Action import Action
from backend.mechanics.Distributor import Distributor
from frontend.GeneralUtils import GeneralUtils
from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering

class BuildSettlement(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        self.data = data
        self.hexagon_rendering = chaperone.current_phase.hexagon_rendering

        ### Following two lines necessary to work with client-side versions of objects
        node = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_NODE, data['node'].id)
        settlement = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_SETTLEMENT, data['settlement'].id)
        node.add_settlement(settlement)

        in_settling_phase = GeneralUtils.safe_isinstance(self.game_phase, 'SettlingPhase')
        if not in_settling_phase:
            ### Update active player client side (to reflect paid for action)
            if self.chaperone.player.id == data['player'].id:
                self.chaperone.player.__dict__ = data['player'].__dict__

        self.update_gui()
    
    def update_gui(self):
        is_instigating_client = self.data['player'].id == self.chaperone.player.id
        in_settling_phase = GeneralUtils.safe_isinstance(self.game_phase, 'SettlingPhase')
        if is_instigating_client:
            self.hexagon_rendering.handle_leave(event = None)
        else:
            self.hexagon_rendering.draw_board_items()

        text_area = self.game_phase.text_area if in_settling_phase else self.game_phase.notebook_frame_handlers['history'].text_area
        text_area.config(state = 'normal')
        node = self.data['settlement'].node
        port_text = ''
        if (port := node.port):
            a_an = 'an' if port.type.startswith(tuple('aeiou')) else 'a'
            port_text = f' on {a_an} {port.type} port'
        nominal_value = node.nominal_value()
        def fun(d, x): d[x[0]] = d.get(x[0], 0) + x[1]; return d
        d = functools.reduce(fun, [(hexagon.resource_type, hexagon.num_pips) for hexagon in node.hexagons], {})
        nominal_values = ' + '.join(f'{v} {k}' for k, v in d.items() if k != 'desert')
        text_to_insert = f'{self.data["player"].name} built a settlement{port_text}! This settlement has a nominal value of {nominal_value} ({nominal_values}).'
        text_area.insert('end', f'\n\n{text_to_insert}')
        text_area.yview('end')
        text_area.config(state = 'disabled')

        if in_settling_phase:
            self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_ROAD
            self.game_phase.instruction_text.set('Build a road!')
        else: ### In main game phase
            play_frame_handler = self.game_phase.notebook_frame_handlers['play']
            action_tree_handler = play_frame_handler.action_tree_handler
            action_tree_handler.cancel(event = None)
            play_frame_handler.update_resource_cards()
            play_frame_handler.update_movable_pieces()
            action_tree_handler.fill_action_tree()
