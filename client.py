import multiprocessing
import socket
import threading

from ClientServerInterface import ClientServerInterface
from actions.ActionFactory import ActionFactory
from frontend.Tkinter.Chaperone import Chaperone
from frontend.Tkinter.phases.setup.sub_phases.HomePhase import HomePhase

class Client:
    LOCAL_HOST = '127.0.0.1'
    LOCAL_PORT = 9090

    def __init__(self):
        self.interface = ClientServerInterface()
        self.games = {}
        self.host = self.LOCAL_HOST
        self.port = self.LOCAL_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.queue = multiprocessing.Queue()
        self.receive_thread = threading.Thread(target = self.receive)
        self.gui_thread = threading.Thread(target = self.gui)
        self.receive_thread.start()
        self.gui_thread.start()
    
    def receive(self):
        while True:
            try:
                data = self.interface.receive_data(self.socket)
                if data:
                    self.queue.put(data)
            except:
                self.queue.put({'action': ActionFactory.END_GAME})

    def gui(self):
        self.chaperone = Chaperone(self, self.queue)
        self.chaperone.start_phase(HomePhase)

client = Client()