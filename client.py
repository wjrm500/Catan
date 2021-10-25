from frontend.Tkinter.Chaperone import Chaperone
import socket
import threading

class Client:
    LOCAL_HOST = '127.0.0.1'
    LOCAL_PORT = 9090

    def __init__(self):
        self.games = {}
        self.host = self.LOCAL_HOST
        self.port = self.LOCAL_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        # self.receive_thread = threading.Thread(target = self.receive)
        self.gui_thread = threading.Thread(target = self.gui)
        # self.receive_thread.start()
        self.gui_thread.start()
    
    ### NEED TO BE ABLE TO RECEIVE MESSAGES ASYNCHRONOUSLY WHILE ALSO BEING ABLE TO RECEIVE MESSAGES ON DEMAND
    # def receive(self):
    #     while True:
    #         from_server = self.socket.recv(1024)
    #         ### Receive broadcast from server and do something e.g. new player added

    def gui(self):
        self.chaperone = Chaperone(self.socket)
        self.chaperone.start_home_phase()

client = Client()