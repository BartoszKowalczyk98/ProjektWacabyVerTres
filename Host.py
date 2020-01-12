import pickle
import socket
import sys
from time import sleep

import pymsgbox
from _thread import start_new_thread

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
    def __init__(self,conn , plansza: Board):
        QThread.__init__(self)
        self.conn = conn
        self.plansza = plansza

    def run(self):
        print("kogos zaakceptowało ale przed 1 wyslaniem")
        toBeSent = self.plansza.encodeBoard()
        self.conn.send(pickle.dumps(toBeSent))  # wysłanie board'a w ramach rozpoczęcia gry
        print("po 1 wyslaniu")
        while True:
            try:
                print("przed wczytaniem")
                data = pickle.loads(conn.recv(10000))
                print("po wczytaniu")
                self.plansza.decodeBoard(data)
                while self.plansza.myTurn:
                    sleep(0.5)
                if not data:
                    print("disconnected")
                    sys.exit()
                    break
                else:
                    print("przed wysłaniem")
                    toBeSent = self.plansza.encodeBoard()
                    self.conn.sendall(pickle.dumps(toBeSent))
                    print("po wysłaniu")
            except:
                print("eror")
                break
        print("lost connection")
        self.conn.close()

print("przed akceptacja")
pymsgbox.alert('Waiting for opponent to connect', 'Be patient...')
conn, addr = s.accept()  # conn to jest ponoc to polaczenie cos ala socket w javie bo przez niego sie przesyla

print("connected to: ", addr)
app = QApplication(sys.argv)
b = Board("host","player")
mythread = threaded_client(conn,b)
mythread.start()
app.exec()
