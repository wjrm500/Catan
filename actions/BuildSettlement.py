import functools

from actions.Action import Action
from backend.mechanics.Distributor import Distributor
from frontend.GeneralUtils import GeneralUtils as gutils
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
        self.node = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_NODE, data['node_id'])
        settlement = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_SETTLEMENT, data['settlement_id'])
        self.node.add_settlement(settlement)

        in_settling_phase = gutils.safe_isinstance(self.game_phase, 'SettlingPhase')
        if not in_settling_phase:
            self.reload_all_players() ### Not just active player because victory points etc. change

        self.update_gui()
    
    def update_gui(self):
        in_settling_phase = gutils.safe_isinstance(self.game_phase, 'SettlingPhase')
        if self.is_instigating_client():
            self.hexagon_rendering.handle_leave(event = None)
        else:
            self.hexagon_rendering.draw_board_items()

        text_area = self.get_text_area(in_settling_phase)
        self.enable_text_area(text_area)

        port_text = ''
        if (port := self.node.port):
            a_an = 'an' if port.type.startswith(tuple('aeiou')) else 'a'
            port_text = f' on {a_an} {port.type} port'
        nominal_value = self.node.nominal_value()
        def fun(d, x): d[x[0]] = d.get(x[0], 0) + x[1]; return d
        d = functools.reduce(fun, [(hexagon.resource_type, hexagon.num_pips) for hexagon in self.node.hexagons], {})
        nominal_values = ' + '.join(f'{v} {k}' for k, v in d.items() if k != 'desert')
        text_to_insert = f'{self.data["player"].name} built a settlement{port_text}! This settlement has a nominal value of {nominal_value} ({nominal_values}).'
        text_area.insert('end', f'\n\n{text_to_insert}', 'green_font')

        self.disable_text_area(text_area)

        if in_settling_phase:
            self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_ROAD
            self.game_phase.instruction_text.set('Build a road!')
        else: ### In main game phase
            self.refresh_play_frame_handler()
            self.refresh_status_frame_handler()