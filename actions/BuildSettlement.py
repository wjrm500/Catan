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

        self.update_gui()
    
    def update_gui(self):
        is_instigating_client = self.data['player'].id == self.chaperone.player.id
        in_settling_phase = GeneralUtils.safe_isinstance(self.game_phase, 'SettlingPhase')
        if is_instigating_client:
            self.hexagon_rendering.handle_leave(event = None)
            if in_settling_phase:
                self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_ROAD
                self.game_phase.instruction_text.set('Build a road!')
        else:
            self.hexagon_rendering.draw_board_items()
        text_area = self.game_phase.text_area
        text_area.config(state = 'normal')
        node = self.data['settlement'].node
        port_text = ''
        if (port := node.port):
            a_an = 'an' if port.type.startswith(tuple('aeiou')) else 'a'
            port_text = f' on {a_an} {port.type} port'
        nominal_value = node.nominal_value()
        nominal_values = ' + '.join([f'{hexagon.num_pips} {hexagon.resource_type}' for hexagon in node.hexagons if hexagon.resource_type != 'desert'])
        text_to_insert = f'{self.data["player"].name} built a settlement{port_text}! This settlement has a nominal value of {nominal_value} ({nominal_values}).'
        text_area.insert('end', f'\n\n{text_to_insert}')
        text_area.yview('end')
        text_area.config(state = 'disabled')