import pickle
import socket
import sys
from time import sleep

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

from Board import Board

server = "10.1.202.141"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("waiting for connection, server started!")


class threaded_client(QThread):  # obsługa klienta
    def __init__(self, conn, plansza: Board):
        QThread.__init__(self)
        self.conn = conn
        self.plansza = plansza

    def run(self):
        toBeSent = self.plansza.encodeBoard()
        self.conn.send(pickle.dumps(toBeSent))
        while True:
            data = pickle.loads(conn.recv(10000))
            self.plansza.decodeBoard(data)
            while self.plansza.myTurn:
                if self.plansza.surrenderBool:
                    self.conn.sendall(pickle.dumps(self.plansza.surrenderBool))
                    return
                sleep(0.5)
            if not data:
                print("disconnected")
                sys.exit()
                break
            else:
                toBeSent = self.plansza.encodeBoard()
                self.conn.sendall(pickle.dumps(toBeSent))

        print("lost connection")
        self.conn.close()


conn, addr = s.accept()  # conn to jest ponoc to polaczenie cos ala socket w javie bo przez niego sie przesyla

print("connected to: ", addr)
app = QApplication(sys.argv)
b = Board("host", "player")
mythread = threaded_client(conn, b)
mythread.start()
app.exec()
