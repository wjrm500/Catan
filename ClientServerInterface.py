import json
import pickle

from pympler.asizeof import asizeof

class ClientServerInterface:
    def send_data(self, recipient, message):
        try:
            encoded_message = json.dumps(message).encode('utf-8')
        except:
            encoded_message = pickle.dumps(message)
        bytes_to_send = str(asizeof(encoded_message)).encode('utf-8')
        recipient.send(bytes_to_send) ### Header
        recipient.send(encoded_message)

    def receive_data(self, socket):
        data = {}
        from_recipient = socket.recv(16) ### Header
        bytes_to_receive = from_recipient.decode('utf-8')
        if bytes_to_receive and bytes_to_receive.isnumeric():
            data = socket.recv(int(bytes_to_receive))
            try:
                data = data.decode('utf-8')
                data = json.loads(data)
            except:
                data = pickle.loads(data)
        return data