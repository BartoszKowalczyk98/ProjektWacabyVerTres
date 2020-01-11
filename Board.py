from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MyPushButton import MyPushButton
from MyEnum import RodzajPionka

class Board:
    def __init__(self):
        super(Board, self).__init__()
        self.isPieceSelected = False
        self.board = []
        self.tempbutton = None
        self.initUI()

    def uncheckall(self):
        for i in range (0,8):
            self.grupy[i].setExclusive(False)
            for j in range(1,9):
                self.grupy[i].button(j).setChecked(False)
            self.grupy[i].setExclusive(True)


    def buttonpressed(self):
        for i in range (0,8):
            self.tempbutton = self.grupy[i].checkedButton()
            tempint = (i,self.grupy[i].checkedId())
            if self.tempbutton is not None:
                break
        self.uncheckall()
        print(self.tempbutton.getKind(), " koordynaty: ",tempint)
        #print("Wcisniety przycisk:", chr(ord('A') + tempint[0]), tempint[1])
        print(self.boardAsArray)
        self.boardAsArray[tempint[0]+tempint[1]-1] = RodzajPionka.pusty
        self.updateboard(self.boardAsArray)
        #self.updateboard([0,1,2,0,0,0,1,2,2,1,0,0,0,0,1,2,0,0,0,1,0,2,1,2,2,0,1,1,1,0,3,4])

    def updateboard(self, tablica):
        counter = 0
        if len(tablica) != 32:
            print("Tablica jest nie teges")
        else:
            for i in tablica:
                if (i == RodzajPionka.pusty):
                    self.goodbuttons[counter].setStyleSheet("background-color: gray")
                elif (i == RodzajPionka.bialyzwykly):
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/białyzwykły50.jpg)")
                elif (i == RodzajPionka.czarnyzwykly):
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/czarnyzwykły50.jpg)")
                elif (i == RodzajPionka.bialydama):
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/białadama50.jpg)")
                elif (i == RodzajPionka.czarnydama):
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/czarnadama50.jpg)")
                counter = counter + 1

    def initUI(self):
        self.mainwidget = QWidget()
        self.mainwidget.setFixedSize(600,600)
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.mainwidget.setLayout(self.grid)
        self.grupy = []
        self.goodbuttons = []
        self.boardAsArray = []
        for i in range (0,8):
            self.grupy.append(QButtonGroup())
            self.grupy[i].setExclusive(True)
        for i in range(0,8):
            for j in range(0,8):
                button = MyPushButton(0)
                button.setCheckable(True)
                if ((i+j)%2 == 1 and i >= 0 and i < 3):
                    button.setStyleSheet("background-image: url(assets/białyzwykły50.jpg)")
                    button.setKind(RodzajPionka.bialyzwykly)
                    self.boardAsArray.append(RodzajPionka.bialyzwykly)
                    self.goodbuttons.append(button)
                elif ((i + j) % 2 == 1 and i >= 5 and i < 9):
                    button.setStyleSheet("background-image: url(assets/czarnyzwykły50.jpg)")
                    button.setKind(RodzajPionka.czarnyzwykly)
                    self.boardAsArray.append(RodzajPionka.czarnyzwykly)
                    self.goodbuttons.append(button)
                elif ((i + j) % 2 == 1):
                    button.setStyleSheet("background-color: gray")
                    self.boardAsArray.append(RodzajPionka.pusty)
                    self.goodbuttons.append(button)
                else:
                    button.setStyleSheet("background-color: white")
                    button.setEnabled(False)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.grupy[i].addButton(button, j+1)
                self.grid.addWidget(button, i, j)

        #print(self.grupy[1].button(1).getKind())
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