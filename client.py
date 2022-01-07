from argparse import ArgumentParser
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
    REMOTE_HOST = '13.212.173.98'
    REMOTE_PORT = 9090

    def __init__(self, locally_hosted):
        self.interface = ClientServerInterface()
        self.games = {}
        self.host = self.LOCAL_HOST if locally_hosted else self.REMOTE_HOST
        self.port = self.LOCAL_PORT if locally_hosted else self.REMOTE_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.queue = multiprocessing.Queue()
        self.receive_thread = threading.Thread(target = self.receive)
        # self.gui_thread = threading.Thread(target = self.gui)
        self.receive_thread.start()
        self.gui()
        # self.gui_thread.start()
    
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

parser = ArgumentParser()
parser.add_argument('-l', '--local', dest = 'locally_hosted', help = 'Is server hosted locally?', action = 'store_true')
args = parser.parse_args()
client = Client(args.locally_hosted)