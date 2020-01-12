import sys
from _thread import start_new_thread
from time import sleep

from PyQt5.QtWidgets import QApplication
from Board import Board
from Network import Network


print("1")
n = Network()
print("2")
app = QApplication(sys.argv)
print("3")
board = Board("player","Host")
print("4")
board = n.getP()
print("5")


def threaded_cos(n,b):
    while True:
        print("penis")

start_new_thread(threaded_cos,(n,board))
print("6")
app.exec()


