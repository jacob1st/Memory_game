import socket
import pickle

class Network:
    def __init__(self):
        """Create a socket object and have it make a connection."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 7777  # Change this and the self.ip_address to match whatever is in the server file
        self.ip_address = "" 
        self.addr = (self.ip_address, self.port)
        self.p = self.try_connect()
    
    def get_player(self):
        return int(self.p)

    def try_connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode('utf-8')
        except:
            print("Couldn't connect")

    def send(self, pos):
        # sends a string to the server and receives an object
        try:
            self.client.send(pos.encode('utf-8'))
            return pickle.loads(self.client.recv(2048*4))
        except:
            pass
        