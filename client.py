import multiprocessing
import socket
import threading
import time

from ClientServerInterface import ClientServerInterface
from actions.ActionFactory import ActionFactory
from frontend.Tkinter.Chaperone import Chaperone
from frontend.Tkinter.phases.setup.sub_phases.HomePhase import HomePhase
import server

class Client:
    HOST = ''
    PORT = 9090

    def __init__(self):
        self.interface = ClientServerInterface()
        self.queue = multiprocessing.Queue()
        self.gui()
    
    def serve(self):
        self.serve_thread = threading.Thread(target = server.serve)
        self.serve_thread.start()
    
    def connect(self, host = None):
        time.sleep(1)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = host or socket.gethostbyname(socket.gethostname())
        self.socket.connect((host, self.PORT))
        self.receive_thread = threading.Thread(target = self.receive)
        self.receive_thread.start()
    
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