from tkinter import ttk

from frontend.Tkinter.phases.Phase import Phase

class Style:
    def setup(self):
        style = ttk.Style()
        blue = Phase.BG_COLOR
        darker_blue = Phase.DARKER_BG_COLOR

        style.theme_create('catan', parent = 'classic', settings = { ### Need classic to avoid dashed lines on selected notebook tab
            'TNotebook': {
                'configure': {'background': blue, 'tabmargins': [0, 0]}
            },
            'TNotebook.Tab': {
                'configure': {'background': blue, 'padding': [5, 5]},
                'map': {'background': [('selected', darker_blue)]}
            },
            'Treeview': {
                'configure': {'background': blue, 'fieldbackground': blue}
            },
            'Treeview.Heading': {
                'configure': {'background': blue, 'font': ('Arial', 10, 'bold')}
            }
        })
        style.theme_use('catan')

        ### Style scrollbar
        style.element_create('My.Vertical.TScrollbar.trough', 'from', 'clam')
        style.element_create('My.Vertical.TScrollbar.thumb', 'from', 'clam')
        style.element_create('My.Vertical.TScrollbar.grip', 'from', 'clam')
        style.layout('My.Vertical.TScrollbar', [('My.Vertical.TScrollbar.trough', {'children': [('My.Vertical.TScrollbar.thumb', {'unit': '1', 'children': [('My.Vertical.TScrollbar.grip', {'sticky': ''})], 'sticky': 'nswe'})], 'sticky': 'ns'})])

        style.configure('StatusFrame.Treeview.Heading', background = Phase.DARKER_BG_COLOR)
        style.configure('StatusFrame.Treeview', background = Phase.DARKER_BG_COLOR, borderwidth = 0)