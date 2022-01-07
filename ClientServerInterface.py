import json
import pickle
import struct

class ClientServerInterface:
    def send_data(self, recipient, message):
        try:
            encoded_message = json.dumps(message).encode('utf-8')
        except:
            encoded_message = pickle.dumps(message)
        self.send_msg(recipient, encoded_message)

    def receive_data(self, socket):
        data = self.recv_msg(socket)
        try:
            data = data.decode('utf-8')
            data = json.loads(data)
        except:
            data = pickle.loads(data)
        return data
    
    ### Credit to Stack Overflow user Adam Rosenfield for following functions
    ### https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
    def send_msg(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data