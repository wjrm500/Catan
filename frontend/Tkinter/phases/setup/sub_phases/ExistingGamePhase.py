import tkinter
from frontend.Tkinter.phases.setup.SetupPhase import SetupPhase

class ExistingGamePhase(SetupPhase):
    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.ip_address_label = self.render_label(where = self.inner_frame, text = 'IP address:')
        self.ip_address_input = self.render_input(where = self.inner_frame)
        self.submit_button = self.render_button(where = self.inner_frame, text = 'Submit')
        inner_frame_components = [self.ip_address_label, self.ip_address_input, self.submit_button]
        for component in inner_frame_components:
            component.pack(side = tkinter.TOP, pady = 20)
        self.ip_address_input.focus()

    def run(self):
        self.submit_button.bind('<Motion>', lambda evt: self.root.configure(cursor = self.CURSOR_HAND))
        self.submit_button.bind('<Leave>', lambda evt: self.root.configure(cursor = self.CURSOR_DEFAULT))
        self.submit_button.bind('<Button-1>', self.submit_form)
        self.ip_address_input.bind('<Return>', self.submit_form)
        self.root.mainloop()
    
    def submit_form(self, event):
        ip_address = self.ip_address_input.get()
        try:
            self.chaperone.client.connect(ip_address)
            self.chaperone.join_existing_game(ip_address)
        except:
            self.display_error_text('Invalid IP address')
    
    def display_error_text(self, error_text):
        if hasattr(self, 'error_text'):
            self.error_text.destroy()
        self.error_text = self.render_error_text(self.inner_frame, error_text)
        self.error_text.pack(side = tkinter.TOP, pady = 10)