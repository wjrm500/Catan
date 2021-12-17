import tkinter
from frontend.GeneralUtils import GeneralUtils as gutils
from frontend.Tkinter.phases.Phase import Phase
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.BaseFrameHandler import BaseFrameHandler

class StatusFrameHandler(BaseFrameHandler):
    def __init__(self, phase, notebook):
        super().__init__(phase, notebook)
        self.num_players = len(self.phase.chaperone.player.game.players)
        self.text_variables = {
            'Victory points': [{'text': tkinter.StringVar(), 'label': None} for _ in range(self.num_players)],
            'Largest army': [{'text': tkinter.StringVar(), 'label': None} for _ in range(self.num_players)],
            'Longest road': [{'text': tkinter.StringVar(), 'label': None} for _ in range(self.num_players)]
        }
    
    def load_text_variables(self):
        game = self.player.game

        victory_points = [{
            'name': player.name,
            'value': (victory_points := player.victory_points()),
            'ranked_first': victory_points >= game.victory_point_limit
            } for player in game.players]
        sorted_victory_points = sorted(victory_points, key = lambda x: x['value'], reverse = True)

        army_size = [{
            'name': player.name,
            'value': player.army_size,
            'has_largest_army': (has_largest_army := player.has_largest_army()),
            'ranked_first': has_largest_army
            } for player in game.players]
        sorted_army_size = sorted(army_size, key = lambda x: (x['has_largest_army'], x['value']), reverse = True)

        longest_road = [{
            'name': player.name,
            'value': player.longest_road,
            'has_longest_road': (has_longest_road := player.has_longest_road()),
            'ranked_first': has_longest_road
            } for player in game.players]
        sorted_longest_road = sorted(longest_road, key = lambda x: (x['has_longest_road'], x['value']), reverse = True)

        iterable = [
            {'text_variables_index': 'Victory points', 'local_list': sorted_victory_points},
            {'text_variables_index': 'Largest army', 'local_list': sorted_army_size},
            {'text_variables_index': 'Longest road', 'local_list': sorted_longest_road},
        ]
        for item in iterable:
            for i, text_variable in enumerate(self.text_variables[item['text_variables_index']]):
                player_data = item['local_list'][i]
                text = f'{player_data["name"]} - {player_data["value"]}'
                text_variable['text'].set(text)
                bg_color = 'gold' if player_data['ranked_first'] else Phase.DARKER_BG_COLOR
                text_variable['label'].configure(background = bg_color)

    def setup(self):
        self.frame.grid_columnconfigure(0, weight = 1)
        frame_width = self.frame.master.master.winfo_width() ### Get width of inner frame middle right

        top_top_frame = tkinter.Frame(self.frame, background = Phase.BG_COLOR)
        top_top_frame.grid(row = 0, column = 0, sticky = 'ew')
        self.rounds_completed_text = tkinter.StringVar()
        self.rounds_completed_text.set('Rounds completed: 0')
        interpunct_label = tkinter.Label(top_top_frame, text = '·', background = Phase.BG_COLOR, foreground = 'gray', font = ('Calibri', 12, 'bold'))
        rounds_completed_label = tkinter.Label(top_top_frame, textvariable = self.rounds_completed_text, background = Phase.BG_COLOR)
        victory_points_required_label = tkinter.Label(top_top_frame, text = f'Victory points required: {self.player.game.victory_point_limit}', background = Phase.BG_COLOR)
        ordinary_wizarding_labels = [rounds_completed_label, victory_points_required_label]
        label_arr = gutils.intersperse(interpunct_label, ordinary_wizarding_labels)
        for label in label_arr:
            label.pack(side = tkinter.LEFT)

        top_frame = tkinter.Frame(self.frame, background = Phase.BG_COLOR)
        top_frame.grid(row = 1, column = 0, sticky = 'ew')
        top_frame.grid_rowconfigure(0, weight = 1)
        iterable = [
            {'title': 'Victory points', 'highlightthickness': 2},
            {'title': 'Largest army', 'highlightthickness': 0},
            {'title': 'Longest road', 'highlightthickness': 0}
        ]
        for i, item in enumerate(iterable):
            top_frame.grid_columnconfigure(i, weight = 1, uniform = 'catan')
            sub_frame = tkinter.Frame(top_frame, background = Phase.DARKER_BG_COLOR, highlightbackground = 'black', highlightthickness = item['highlightthickness'], width = round(frame_width / 10))
            sub_frame.grid(row = 0, column = i, padx = 2.5, pady = 2.5)
            title_label = tkinter.Label(sub_frame, text = item['title'], background = Phase.DARKER_BG_COLOR, width = round(frame_width / 20), font = ('Arial', 10, 'bold'))
            title_label.pack(pady = 5)
            for i in range(self.num_players):
                text_variable = self.text_variables[item['title']][i]
                player_label = tkinter.Label(sub_frame, textvariable = text_variable['text'], background = Phase.DARKER_BG_COLOR)
                player_label.pack(anchor = tkinter.CENTER, side = tkinter.TOP)
                text_variable['label'] = player_label
        self.load_text_variables()