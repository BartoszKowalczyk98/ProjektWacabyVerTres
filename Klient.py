import sys
import socket
import pickle
from time import sleep

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from Board import Board

print("1")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "10.1.202.141"
port = 5555
addr = (server,port)
client.connect(addr)


print("2")
app = QApplication(sys.argv)
print("3")
board = Board("player","host")
print("4")


class myThread(QThread):
    def __init__(self, plansza: Board):
        QThread.__init__(self)
        self.plansza = plansza
    def run(self):
        data = pickle.loads(client.recv(10000))
        self.plansza.decodeBoard(data)
        while True:
            while self.plansza.myTurn:
                sleep(0.5)
            tobesent = self.plansza.encodeBoard()
            client.sendall(pickle.dumps(tobesent))
            data = pickle.loads(client.recv(10000))
            if not data:
                print("disconnected")
            else:
                self.plansza.decodeBoard(data)



print("6")
app.exec()


