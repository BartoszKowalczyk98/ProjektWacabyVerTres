# todo to będzie klasa board bo to bedzie przesylane miedzy "klientem a hostem"
import sys

from PyQt5.QtWidgets import QApplication

from Board import Board

if __name__ == '__main__':
    print("hello")
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    b = Board()
    app.exec()
