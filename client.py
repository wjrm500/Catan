from frontend.Tkinter.Chaperone import Chaperone
import socket
import threading
import multiprocessing
import pickle
import json

from frontend.Tkinter.phases.setup.sub_phases.HomePhase import HomePhase

class Client:
    LOCAL_HOST = '127.0.0.1'
    LOCAL_PORT = 9090

    def __init__(self):
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
            from_server = self.socket.recv(16)
            bytes_to_receive = from_server.decode('utf-8')
            if bytes_to_receive and bytes_to_receive.isnumeric():
                data = self.socket.recv(int(bytes_to_receive))
                try:
                    data = data.decode('utf-8')
                    data = json.loads(data)
                except:
                    data = pickle.loads(data)
                self.queue.put(data)

    def gui(self):
        self.chaperone = Chaperone(self.socket, self.queue)
        self.chaperone.start_phase(HomePhase)

client = Client()