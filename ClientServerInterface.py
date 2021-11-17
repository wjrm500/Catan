import json
import pickle

from pympler.asizeof import asizeof

from backend.mechanics.Distributor import Distributor

class ClientServerInterface:
    def send_data(self, recipient, message):
        try:
            encoded_message = json.dumps(message).encode('utf-8')
        except:
            try:
                encoded_message = pickle.dumps(message)
            except:
                serializable_message = self.get_serializable_message(message)
                encoded_message = pickle.dumps(serializable_message)
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
    
    def get_serializable_message(self, message):
        ### The first custom recursive function I've built that actually works!!!
        ### Removes any unserializable properties from any objects in the message
        if isinstance(message, dict):
            to_return = {}
            for key, value in message.items():
                if not isinstance(value, list) and not isinstance(value, dict):
                    if isinstance(value, object):
                        if hasattr(value, 'get_serializable_copy') and callable(getattr(value, 'get_serializable_copy')):
                            to_return[key] = value.get_serializable_copy()
                        else:
                            to_return[key] = value
                else:
                    to_return[key] = self.get_serializable_message(value)
        elif isinstance(message, list):
            to_return = []
            for value in message:
                if not isinstance(value, list) and not isinstance(value, dict):
                    if isinstance(value, object):
                        if hasattr(value, 'get_serializable_copy') and callable(getattr(value, 'get_serializable_copy')):
                            to_return.append(value.get_serializable_copy())
                        else:
                            to_return.append(value)
                else:
                    to_return.append(self.get_serializable_message(value))
        return to_return
    
    @staticmethod
    def replace_object_in_distributor(distributor, object_type, new_object):
        if object_type == Distributor.OBJ_HEXAGON:
            distributor.hexagons = [existing_hexagon for existing_hexagon in distributor.hexagons if existing_hexagon.id != new_object.id]
            distributor.hexagons.append(new_object)
        elif object_type == Distributor.OBJ_LINE:
            distributor.lines = [existing_line for existing_line in distributor.lines if existing_line.id != new_object.id]
            distributor.lines.append(new_object)
        elif object_type == Distributor.OBJ_NODE:
            distributor.nodes = [existing_node for existing_node in distributor.nodes if existing_node.id != new_object.id]
            distributor.nodes.append(new_object)