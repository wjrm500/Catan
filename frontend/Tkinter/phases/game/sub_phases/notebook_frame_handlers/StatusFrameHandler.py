import tkinter
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
    
    def setup(self):
        self.frame.grid_columnconfigure(0, weight = 1)
        frame_width = self.frame.master.master.winfo_width() ### Get width of inner frame middle right
        top_frame = tkinter.Frame(self.frame, background = Phase.BG_COLOR)
        top_frame.grid(row = 0, column = 0, sticky = 'ew')
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