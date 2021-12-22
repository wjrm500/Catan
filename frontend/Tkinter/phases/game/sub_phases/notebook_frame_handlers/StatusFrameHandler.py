from collections import Counter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, MaxNLocator
import tkinter
from tkinter import ttk

from config import config
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
        self.canvas = tkinter.Canvas(self.frame, bd = 0, highlightthickness = 0, background = 'red')
        scrollbar = ttk.Scrollbar(self.frame, orient = 'vertical', command = self.canvas.yview, style = 'My.Vertical.TScrollbar')
        self.canvas.pack(side = tkinter.LEFT, expand = True, fill = 'both')
        self.canvas.bind('<Configure>', self.FrameWidth)
        scrollbar.pack(side = tkinter.RIGHT, fill = 'y')

        self.scrollable_frame = tkinter.Frame(self.canvas)
        self.scrollable_frame.bind('<Configure>', lambda evt: self.canvas.configure(scrollregion = self.canvas.bbox('all')))
        
        self.scrollable_frame.pack(expand = True, fill = 'both')
        self.canvas_frame = self.canvas.create_window((0, 0), window = self.scrollable_frame, anchor = tkinter.NW)
        self.canvas.configure(yscrollcommand = scrollbar.set)
    
    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

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
        self.scrollable_frame.grid_columnconfigure(0, weight = 1)
        frame_width = self.frame.master.master.winfo_width() ### Get width of inner frame middle right

        top_top_frame = tkinter.Frame(self.scrollable_frame, background = Phase.BG_COLOR)
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

        top_frame = tkinter.Frame(self.scrollable_frame, background = Phase.BG_COLOR)
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
            sub_frame.grid(row = 0, column = i, padx = 5, pady = 2.5)
            title_label = tkinter.Label(sub_frame, text = item['title'], background = Phase.DARKER_BG_COLOR, width = round(frame_width / 20), font = ('Arial', 10, 'bold'))
            title_label.pack(pady = 5)
            for i in range(self.num_players):
                text_variable = self.text_variables[item['title']][i]
                player_label = tkinter.Label(sub_frame, textvariable = text_variable['text'], background = Phase.DARKER_BG_COLOR)
                player_label.pack(anchor = tkinter.CENTER, side = tkinter.TOP)
                text_variable['label'] = player_label
        self.load_text_variables()

        self.load_dice_roll_num_distro_frame()
        self.load_resource_potential_frame()
        self.load_resources_won_frame()

    def load_dice_roll_num_distro_frame(self):
        game = self.player.game
        roll_num_dict = dict(Counter(game.dice_rolls))
        roll_num_freqs = {i: roll_num_dict.get(i, 0) for i in range(2, 13)}
        x = list(roll_num_freqs.keys())
        y = list(roll_num_freqs.values())
        if not roll_num_dict:
            return
        if hasattr(self, 'roll_num_distro_frame'):
            self.roll_num_distro_frame.destroy()
        outer_frame = tkinter.Frame(self.scrollable_frame, background = Phase.BG_COLOR, padx = 5, pady = 5)
        outer_frame.grid(row = 2, column = 0, sticky = 'ew')
        self.roll_num_distro_frame = tkinter.Frame(outer_frame, background = Phase.DARKER_BG_COLOR, height = 1)
        self.roll_num_distro_frame.pack(fill = 'x', side = tkinter.TOP)
        figure = plt.Figure(figsize = (2, 2), dpi = 100, facecolor = Phase.DARKER_BG_COLOR)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, self.roll_num_distro_frame)
        chart_type.get_tk_widget().pack(expand = True, fill = 'both', padx = 2.5, pady = 10)
        ax.set_title('Dice roll number distribution', fontdict = {'fontname': 'Arial', 'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylim(bottom = 0, top = max(roll_num_freqs.values()) + 1)
        ax.set_facecolor(Phase.DARKER_BG_COLOR)
        ax.tick_params(axis = 'both', labelsize = 8)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontname('Arial')
        ax.set_xticks(x)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))
        ax.yaxis.set_major_locator(MaxNLocator(integer = True))
        ax.bar(x, y, color = Phase.BG_COLOR)
    
    def load_resource_potential_frame(self):
        outer_frame = tkinter.Frame(self.scrollable_frame, background = Phase.BG_COLOR, padx = 5, pady = 5)
        outer_frame.grid(row = 3, column = 0, sticky = 'ew')
        top_label = tkinter.Label(outer_frame, text = 'Resource potential (total num. pips)', background = Phase.DARKER_BG_COLOR, anchor = tkinter.W, font = ('Arial', 10, 'bold'))
        top_label.pack(fill = 'x', side = tkinter.TOP)
        bottom_frame = tkinter.Frame(outer_frame, background = Phase.DARKER_BG_COLOR)
        bottom_frame.pack(fill = 'x', side = tkinter.TOP)
        game = self.player.game
        resource_types = [resource_type for resource_type in list(config['resource_types'].keys()) if resource_type != 'desert']
        columns = ['player'] + resource_types + ['total']
        self.resource_potential_table = ttk.Treeview(bottom_frame, columns = columns, show = 'headings', style = 'StatusFrame.Treeview', height = len(game.players))
        for column in columns:
            self.resource_potential_table.heading(column, text = column.title(), anchor = tkinter.W)
            self.resource_potential_table.column(column, width = 5)
        for player in game.players:
            pip_dict = player.pip_dict()
            tree_values = [player.name] + [str(x) for x in pip_dict.values()] + [str(sum(pip_dict.values()))]
            self.resource_potential_table.insert('', tkinter.END, iid = player.name, text = player.name, values = tree_values)
            
        self.resource_potential_table.pack(expand = True, fill = 'x', side = tkinter.TOP)
    
    def update_resource_potential_frame(self):
        self.resource_potential_table.delete(*self.resource_potential_table.get_children())
        game = self.player.game
        for player in game.players:
            pip_dict = player.pip_dict()
            tree_values = [player.name] + [str(x) for x in pip_dict.values()] + [str(sum(pip_dict.values()))]
            self.resource_potential_table.insert('', tkinter.END, iid = player.name, text = player.name, values = tree_values)
    
    def load_resources_won_frame(self):
        outer_frame = tkinter.Frame(self.scrollable_frame, background = Phase.BG_COLOR, padx = 5, pady = 5)
        outer_frame.grid(row = 4, column = 0, sticky = 'ew')
        top_label = tkinter.Label(outer_frame, text = 'Resources won', background = Phase.DARKER_BG_COLOR, anchor = tkinter.W, font = ('Arial', 10, 'bold'))
        top_label.pack(fill = 'x', side = tkinter.TOP)
        bottom_frame = tkinter.Frame(outer_frame, background = Phase.DARKER_BG_COLOR)
        bottom_frame.pack(fill = 'x', side = tkinter.TOP)
        game = self.player.game
        resource_types = [resource_type for resource_type in list(config['resource_types'].keys()) if resource_type != 'desert']
        columns = ['player'] + resource_types + ['total']
        self.resources_won_table = ttk.Treeview(bottom_frame, columns = columns, show = 'headings', style = 'StatusFrame.Treeview', height = len(game.players))
        for column in columns:
            self.resources_won_table.heading(column, text = column.title(), anchor = tkinter.W)
            self.resources_won_table.column(column, width = 5)
        for player in game.players:
            resources_won_dict = player.resources_won
            tree_values = [player.name] + [str(x) for x in resources_won_dict.values()] + [str(sum(resources_won_dict.values()))]
            self.resources_won_table.insert('', tkinter.END, iid = player.name, text = player.name, values = tree_values)
            
        self.resources_won_table.pack(expand = True, fill = 'x', side = tkinter.TOP)
    
    def update_resources_won_frame(self):
        self.resources_won_table.delete(*self.resources_won_table.get_children())
        game = self.player.game
        for player in game.players:
            resources_won_dict = player.resources_won
            tree_values = [player.name] + [str(x) for x in resources_won_dict.values()] + [str(sum(resources_won_dict.values()))]
            self.resources_won_table.insert('', tkinter.END, iid = player.name, text = player.name, values = tree_values)