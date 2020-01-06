from PyQt5.QtWidgets import *


class Board:
    def __init__(self):
        super(Board, self).__init__()
        self.isPieceSelected = False
        self.board = []
        self.initUI()

    def uncheckall(self):
        for i in range(0, 8):
            self.grupy[i].setExclusive(False)
            for j in range(1, 9):
                self.grupy[i].button(j).setChecked(False)
            self.grupy[i].setExclusive(True)

    def buttonpressed(self):
        for i in range(0, 8):
            tempbutton = self.grupy[i].checkedButton()
            tempint = [i, self.grupy[i].checkedId()]
            if tempbutton is not None:
                break
        self.uncheckall()
        print("Wcisniety przycisk:", chr(ord('A') + tempint[0]), tempint[1])

    def initUI(self):
        self.mainwidget = QWidget()
        self.mainwidget.setFixedSize(600, 600)
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.mainwidget.setLayout(self.grid)
        self.grupy = []
        for i in range(0, 8):
            self.grupy.append(QButtonGroup())
            self.grupy[i].setExclusive(True)
        for i in range(0, 8):
            for j in range(0, 8):
                button = QPushButton()
                button.setCheckable(True)
                if ((i + j) % 2 == 1 and i >= 0 and i < 3):
                    button.setStyleSheet("background-image: url(assets/białyzwykły50.jpg)")
                elif ((i + j) % 2 == 1 and i >= 5 and i < 9):
                    button.setStyleSheet("background-image: url(assets/czarnyzwykły50.jpg)")
                elif ((i + j) % 2 == 1):
                    button.setStyleSheet("background-color: gray")
                else:
                    button.setStyleSheet("background-color: white")
                    button.setEnabled(False)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.grupy[i].addButton(button, j + 1)
                self.grid.addWidget(button, i, j)
        self.mainwidget.show()

        self.grupy[0].buttonClicked.connect(self.buttonpressed)
        self.grupy[1].buttonClicked.connect(self.buttonpressed)
        self.grupy[2].buttonClicked.connect(self.buttonpressed)
        self.grupy[3].buttonClicked.connect(self.buttonpressed)
        self.grupy[4].buttonClicked.connect(self.buttonpressed)
        self.grupy[5].buttonClicked.connect(self.buttonpressed)
        self.grupy[6].buttonClicked.connect(self.buttonpressed)
        self.grupy[7].buttonClicked.connect(self.buttonpressed)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    board = Board()
    sys.exit(app.exec())