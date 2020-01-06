import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.1.202.141"
        self.port = 5555
        self.addr = (self.server, self.port)
        print("debug1")
        self.board = self.connect()

    def getP(self):
        return self.board

    def connect(self):
        try:
            self.client.connect(self.addr)
            print("debug2")
            return pickle.loads(self.client.recv(10000))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(10000))
        except socket.error as e:
            print(e)
