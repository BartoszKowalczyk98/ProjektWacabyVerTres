import sys
import socket
import pickle
from time import sleep

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from Board import Board

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "10.1.202.141"
port = 5555
addr = (server,port)
client.connect(addr)

app = QApplication(sys.argv)
board = Board("player","host")

class myThread(QThread):
    def __init__(self, plansza: Board):
        QThread.__init__(self)
        self.plansza = plansza
    def run(self):
        data = pickle.loads(client.recv(10000))
        self.plansza.decodeBoard(data)
        while True:
            while self.plansza.myTurn:
                if self.plansza.surrenderBool:
                    client.sendall(pickle.dumps(self.plansza.surrenderBool))
                    return
                sleep(0.5)
            tobesent = self.plansza.encodeBoard()
            client.sendall(pickle.dumps(tobesent))
            data = pickle.loads(client.recv(10000))
            if not data:
                print("disconnected")
                client.close()
                sys.exit()
            else:
                self.plansza.decodeBoard(data)



mythread = myThread(board)
mythread.start()
sys.exit(app.exec())


