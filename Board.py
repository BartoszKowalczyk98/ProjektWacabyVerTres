from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MyPushButton import MyPushButton
from MyEnum import RodzajPionka


class Board(QMainWindow):
    def __init__(self):
        super(Board, self).__init__()
        self.isPieceSelected = False
        self.board = []
        self.tempbutton = None
        self.lastclicked = ()
        self.status = self.statusBar()
        self.initUI()

    def uncheckall(self):
        for i in range(0, 8):
            self.grupy[i].setExclusive(False)
            for j in range(1, 9):
                self.grupy[i].button(j).setChecked(False)
            self.grupy[i].setExclusive(True)

    def buttonpressed(self):
        print("Czy bicie jest dostepne?", self.isBeatingPossible("Gracz1"))
        for i in range(0, 8):
            self.tempbutton = self.grupy[i].checkedButton()
            tempint = (i, self.grupy[i].checkedId())
            if self.tempbutton is not None:
                break
        self.uncheckall()
        self.checkMove(tempint)


    def isBeatingPossible(self, user):
        self.status.showMessage('CHUJKURWAKAOSFDKASPFDIOASFPOSDLVKMSPODIFPAESOFKLSPDKOFPSOKDEFPOSEFKSODKFPSDOFPKSPOEF')
        for i in range(0, 8):
            for j in range(0, 8):
                if self.goodbuttons[i * 8 + j].getOwner() == user:
                    if i - 2 >= 0 and j - 2 >= 0 and self.goodbuttons[(i - 1) * 8 + (j - 1)].getOwner() != user and \
                            self.goodbuttons[(i - 1) * 8 + (j - 1)].getOwner() is not None and self.goodbuttons[(i - 2) * 8 + j - 2].getKind() == RodzajPionka.pusty:
                        return True
                    elif i - 2 >= 0 and j + 2 <= 7 and self.goodbuttons[(i - 1) * 8 + (j + 1)].getOwner() != user and \
                            self.goodbuttons[(i - 1) * 8 + (j + 1)].getOwner() is not None and self.goodbuttons[(i - 2) * 8 + j + 2].getKind() == RodzajPionka.pusty:
                        return True
                    elif i + 2 <= 7 and j - 2 >= 0 and self.goodbuttons[(i + 1) * 8 + (j - 1)].getOwner() != user and \
                            self.goodbuttons[(i + 1) * 8 + (j - 1)].getOwner() is not None and self.goodbuttons[(i + 2) * 8 + j - 2].getKind() == RodzajPionka.pusty:
                        return True
                    elif i + 2 <= 7 and j + 2 <= 7 and self.goodbuttons[(i + 1) * 8 + (j + 1)].getOwner() != user and \
                            self.goodbuttons[(i + 1) * 8 + (j + 1)].getOwner() is not None and self.goodbuttons[(i + 2) * 8 + j + 2].getKind() == RodzajPionka.pusty:
                        return True
        return False
    def checkMove(self, tempint):

        if self.lastclicked == tempint:  # odklikanie
            print("odklikanie")
            self.lastclicked = ()
        elif self.lastclicked != ():  # ruch
            if abs(self.lastclicked[1] - tempint[1]) != 1:#no chyba że bicie
                return
            elif self.goodbuttons[
                self.lastclicked[0] * 8 + self.lastclicked[1] - 1].getKind() == RodzajPionka.bialyzwykly:  # jest bialy
                if self.lastclicked[0] - tempint[0] != -1:
                    return
            elif self.goodbuttons[
                self.lastclicked[0] * 8 + self.lastclicked[1] - 1].getKind() == RodzajPionka.czarnyzwykly:
                if self.lastclicked[0] - tempint[0] != 1:
                    return
            if self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].getKind() != RodzajPionka.pusty:
                return
            print("ruch z : ", self.lastclicked, " na ", tempint)
            self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].setKind( self.goodbuttons[
                self.lastclicked[0] * 8 + self.lastclicked[1] - 1].getKind())
            self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].setOwner(self.goodbuttons[self.lastclicked[0] * 8 + self.lastclicked[1] - 1].getOwner())
            self.goodbuttons[self.lastclicked[0] * 8 + self.lastclicked[1] - 1].setKind( RodzajPionka.pusty)
            self.goodbuttons[self.lastclicked[0] * 8 + self.lastclicked[1] - 1].setOwner(None)
            self.lastclicked = ()
            self.updateboard(self.goodbuttons)
        else:  # zaznaczenie co chcemy przesunąć
            if self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].getKind() == RodzajPionka.pusty:
                self.lastclicked = ()
            else:
                print("kliknieto: ", tempint)
                self.lastclicked = tempint

    def updateboard(self, tablica):#tylko do rysowania na ekranie
        counter = 0
        if len(tablica) != 64:
            print("Tablica jest nie teges")
        else:
            for i in tablica:
                if (i.getKind() == RodzajPionka.pusty):
                    self.goodbuttons[counter].setStyleSheet("background-color: gray")
                elif (i.getKind() == RodzajPionka.bialyzwykly):
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/białyzwykły50.jpg)")
                elif (i.getKind() == RodzajPionka.czarnyzwykly):
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/czarnyzwykły50.jpg)")
                elif (i.getKind() == RodzajPionka.bialydama):
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/białadama50.jpg)")
                elif (i.getKind() == RodzajPionka.czarnydama):
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/czarnadama50.jpg)")
                counter = counter + 1

    def initUI(self):
        self.mainwidget = QWidget()
        self.mainwidget.setFixedSize(600, 600)
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.mainwidget.setLayout(self.grid)
        self.grupy = []
        self.goodbuttons = []
        for i in range(0, 8):
            self.grupy.append(QButtonGroup())
            self.grupy[i].setExclusive(True)
        for i in range(0, 8):
            for j in range(0, 8):
                button = MyPushButton(RodzajPionka.pusty)
                button.setCheckable(True)
                if ((i + j) % 2 == 1 and i >= 0 and i < 3):
                    button.setStyleSheet("background-image: url(assets/białyzwykły50.jpg)")
                    button.setKind(RodzajPionka.bialyzwykly)
                    button.setOwner("Gracz1")
                    self.goodbuttons.append(button)
                elif ((i + j) % 2 == 1 and i >= 5 and i < 9):
                    button.setStyleSheet("background-image: url(assets/czarnyzwykły50.jpg)")
                    button.setKind(RodzajPionka.czarnyzwykly)
                    button.setOwner("Gracz2")
                    self.goodbuttons.append(button)
                elif ((i + j) % 2 == 1):
                    button.setStyleSheet("background-color: gray")
                    self.goodbuttons.append(button)
                else:
                    button.setStyleSheet("background-color: white")
                    button.setEnabled(False)
                    button.setKind(RodzajPionka.zablokowany)
                    self.goodbuttons.append(button)

                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.grupy[i].addButton(button, j + 1)
                self.grid.addWidget(button, i, j)

        self.setCentralWidget(self.mainwidget)
        self.show()

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
