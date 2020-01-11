import pickle
import socket
import sys
import pymsgbox
from _thread import start_new_thread

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



def threaded_client(conn, b):  # obsługa klienta
    print("kogos zaakceptowało ale przed 1 wyslaniem")
    conn.send(pickle.dumps(b))  # wysłanie board'a w ramach rozpoczęcia gry
    print("po 1 wyslaniu")
    while True:
        try:
            print("przed wczytaniem")
            data = pickle.loads(conn.recv(10000))
            print("po wczytaniu")
            b = data

            if not data:
                print("disconnected")
                break
            else:
                print("przed wysłaniem")
                conn.sendall(pickle.dumps(b))
                print("po wysłaniu")
        except:
            print("eror")
            break
    print("lost connection")
    conn.close()

print("przed akceptacja")
pymsgbox.alert('Waiting for opponent to connect', 'Be patient...')
conn, addr = s.accept()  # conn to jest ponoc to polaczenie cos ala socket w javie bo przez niego sie przesyla

print("connected to: ", addr)
app = QApplication(sys.argv)
b = Board()
start_new_thread(threaded_client, (conn, b))
app.exec()
