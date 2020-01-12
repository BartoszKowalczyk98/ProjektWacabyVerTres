from _thread import start_new_thread
from time import sleep

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MyPushButton import MyPushButton
from MyEnum import RodzajPionka


class Board(QMainWindow):
    def __init__(self, playername, opponent):
        super(Board, self).__init__()
        self.setWindowTitle(playername)
        self.isPieceSelected = False
        self.board = []
        self.tempbutton = None
        self.lastclicked = ()
        self.playername = playername
        self.myTurn = True
        self.opponent = opponent
        self.status = self.statusBar()
        self.initUI()

    def uncheckall(self):
        for i in range(0, 8):
            self.grupy[i].setExclusive(False)
            for j in range(1, 9):
                self.grupy[i].button(j).setChecked(False)
            self.grupy[i].setExclusive(True)

    def buttonpressed(self):
        if not self.myTurn:
            self.uncheckall()
            return
        for i in range(0, 8):
            self.tempbutton = self.grupy[i].checkedButton()
            tempint = (i, self.grupy[i].checkedId())
            if self.tempbutton is not None:
                break

        self.uncheckall()
        self.checkMove(tempint)


    def isBeatingPossible(self, user):
        self.status.showMessage('Jest możliwość bicia')
        anythingToBeat = False
        for i in range(0, 8):
            for j in range(0, 8):
                if self.goodbuttons[i * 8 + j].getOwner() == user:
                    if i - 2 >= 0 and j - 2 >= 0 and self.goodbuttons[(i - 1) * 8 + (j - 1)].getOwner() != user and \
                            self.goodbuttons[(i - 1) * 8 + (j - 1)].getOwner() is not None and self.goodbuttons[
                        (i - 2) * 8 + j - 2].getKind() == RodzajPionka.pusty:
                        self.tempbutton = self.goodbuttons[(i - 1) * 8 + j - 1]
                        self.changeColor(2)
                        anythingToBeat = True
                    elif i - 2 >= 0 and j + 2 <= 7 and self.goodbuttons[(i - 1) * 8 + (j + 1)].getOwner() != user and \
                            self.goodbuttons[(i - 1) * 8 + (j + 1)].getOwner() is not None and self.goodbuttons[
                        (i - 2) * 8 + j + 2].getKind() == RodzajPionka.pusty:
                        self.tempbutton = self.goodbuttons[(i - 1) * 8 + j + 1]
                        self.changeColor(2)
                        anythingToBeat = True
                    elif i + 2 <= 7 and j - 2 >= 0 and self.goodbuttons[(i + 1) * 8 + (j - 1)].getOwner() != user and \
                            self.goodbuttons[(i + 1) * 8 + (j - 1)].getOwner() is not None and self.goodbuttons[
                        (i + 2) * 8 + j - 2].getKind() == RodzajPionka.pusty:
                        self.tempbutton = self.goodbuttons[(i + 1) * 8 + j - 1]
                        self.changeColor(2)
                        anythingToBeat = True
                    elif i + 2 <= 7 and j + 2 <= 7 and self.goodbuttons[(i + 1) * 8 + (j + 1)].getOwner() != user and \
                            self.goodbuttons[(i + 1) * 8 + (j + 1)].getOwner() is not None and self.goodbuttons[
                        (i + 2) * 8 + j + 2].getKind() == RodzajPionka.pusty:
                        self.tempbutton = self.goodbuttons[(i + 1) * 8 + j + 1]
                        self.changeColor(2)
                        anythingToBeat = True
        if anythingToBeat == False:
            self.status.showMessage('Normalny ruch')
        return anythingToBeat

    def checkMove(self, tempint):
        doIHaveToBeat = self.isBeatingPossible(self.playername)  # sprawdzanie czy jest bicie
        if self.lastclicked == tempint:  # odklikanie

            self.tempbutton = self.goodbuttons[self.lastclicked[0] * 8 + self.lastclicked[1] - 1]
            self.changeColor(0)
            self.lastclicked = ()
        elif self.lastclicked != ():  # ruch
            if doIHaveToBeat:
                completed = self.beatingMove(tempint)
            else:
                completed = self.noBeatingMove(tempint)
            if not completed:
                self.status.showMessage('Bledny ruch')
                return
            else:
                if doIHaveToBeat== True:
                    self.myTurn = True
                else:
                    self.myTurn = False
        else:  # zaznaczenie co chcemy przesunąć
            if self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].getKind() == RodzajPionka.pusty:
                self.lastclicked = ()
            elif self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].getOwner() != self.playername:
                self.lastclicked = ()
            else:

                self.tempbutton = self.goodbuttons[tempint[0] * 8 + tempint[1] - 1]
                self.changeColor(1)
                self.lastclicked = tempint

    def beatingMove(self, tempint):
        wektorPrzeskoku = (tempint[0] - self.lastclicked[0], tempint[1] - self.lastclicked[1])
        if abs(wektorPrzeskoku[1]) != 2 or abs(wektorPrzeskoku[0]) != 2:
            return False
        if self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].getKind() != RodzajPionka.pusty:
            return False
        if self.goodbuttons[(self.lastclicked[0] + int(wektorPrzeskoku[0] / 2)) * 8 + (
                self.lastclicked[1] + int(wektorPrzeskoku[1] / 2) - 1)].getOwner() != self.opponent:
            return False

        self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].setKind(self.goodbuttons[
                                                                      self.lastclicked[0] * 8 + self.lastclicked[
                                                                          1] - 1].getKind())
        self.goodbuttons[
            (self.lastclicked[0] + int(wektorPrzeskoku[0] / 2)) * 8 + (
                    self.lastclicked[1] + int(wektorPrzeskoku[1] / 2) - 1)].setKind(RodzajPionka.pusty)
        self.goodbuttons[
            (self.lastclicked[0] + int(wektorPrzeskoku[0] / 2)) * 8 + (
                    self.lastclicked[1] + int(wektorPrzeskoku[1] / 2) - 1)].setOwner(None)
        self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].setOwner(
            self.goodbuttons[self.lastclicked[0] * 8 + self.lastclicked[1] - 1].getOwner())
        self.goodbuttons[self.lastclicked[0] * 8 + self.lastclicked[1] - 1].setKind(RodzajPionka.pusty)
        self.goodbuttons[self.lastclicked[0] * 8 + self.lastclicked[1] - 1].setOwner(None)
        self.lastclicked = ()
        self.updateboard(self.goodbuttons)
        return True

    def noBeatingMove(self, tempint):
        wektorPrzeskoku = (self.lastclicked[0] - tempint[0], abs(self.lastclicked[1] - tempint[1]))
        if wektorPrzeskoku[1] != 1:
            return False
        elif self.goodbuttons[
            self.lastclicked[0] * 8 + self.lastclicked[1] - 1].getKind() == RodzajPionka.bialyzwykly:  # jest bialy
            if wektorPrzeskoku[0] != -1:
                return False
        elif self.goodbuttons[
            self.lastclicked[0] * 8 + self.lastclicked[1] - 1].getKind() == RodzajPionka.czarnyzwykly:
            if wektorPrzeskoku[0] != 1:
                return False
        if self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].getKind() != RodzajPionka.pusty:
            return False
        print("ruch z : ", self.lastclicked, " na ", tempint)
        self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].setKind(self.goodbuttons[
                                                                      self.lastclicked[0] * 8 + self.lastclicked[
                                                                          1] - 1].getKind())
        self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].setOwner(
            self.goodbuttons[self.lastclicked[0] * 8 + self.lastclicked[1] - 1].getOwner())
        self.goodbuttons[self.lastclicked[0] * 8 + self.lastclicked[1] - 1].setKind(RodzajPionka.pusty)
        self.goodbuttons[self.lastclicked[0] * 8 + self.lastclicked[1] - 1].setOwner(None)
        self.lastclicked = ()
        self.updateboard(self.goodbuttons)
        return True

    def changeColor(self, choice):
        if choice == 1:
            if self.tempbutton.getKind() == RodzajPionka.bialyzwykly:
                self.tempbutton.setStyleSheet("background-image: url(assets/highbiałyzwykły50.jpg)")
            elif self.tempbutton.getKind() == RodzajPionka.bialydama:
                self.tempbutton.setStyleSheet("background-image: url(assets/highbiaładama50.jpg)")
            elif self.tempbutton.getKind() == RodzajPionka.czarnyzwykly:
                self.tempbutton.setStyleSheet("background-image: url(assets/highczarnyzwykły50.jpg)")
            elif self.tempbutton.getKind() == RodzajPionka.czarnydama:
                self.tempbutton.setStyleSheet("background-image: url(assets/highczarnadama50.jpg)")
        elif choice == 0:
            if self.tempbutton.getKind() == RodzajPionka.bialyzwykly:
                self.tempbutton.setStyleSheet("background-image: url(assets/białyzwykły50.jpg)")
            elif self.tempbutton.getKind() == RodzajPionka.bialydama:
                self.tempbutton.setStyleSheet("background-image: url(assets/białadama50.jpg)")
            elif self.tempbutton.getKind() == RodzajPionka.czarnyzwykly:
                self.tempbutton.setStyleSheet("background-image: url(assets/czarnyzwykły50.jpg)")
            elif self.tempbutton.getKind() == RodzajPionka.czarnydama:
                self.tempbutton.setStyleSheet("background-image: url(assets/czarnadama50.jpg)")
        elif choice == 2:
            if self.tempbutton.getKind() == RodzajPionka.bialyzwykly:
                self.tempbutton.setStyleSheet("background-image: url(assets/beatbiałyzwykły50.jpg)")
            elif self.tempbutton.getKind() == RodzajPionka.bialydama:
                self.tempbutton.setStyleSheet("background-image: url(assets/beatbiaładama50.jpg)")
            elif self.tempbutton.getKind() == RodzajPionka.czarnyzwykly:
                self.tempbutton.setStyleSheet("background-image: url(assets/beatczarnyzwykły50.jpg)")
            elif self.tempbutton.getKind() == RodzajPionka.czarnydama:
                self.tempbutton.setStyleSheet("background-image: url(assets/beatczarnadama50.jpg)")

    def updateboard(self, tablica):  # tylko do rysowania na ekranie
        counter = 0
        if len(tablica) != 64:
            print("Tablica jest nie teges")
        else:
            for i in tablica:
                if i.getKind() == RodzajPionka.pusty:
                    self.goodbuttons[counter].setStyleSheet("background-color: gray")
                elif i.getKind() == RodzajPionka.bialyzwykly:
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/białyzwykły50.jpg)")
                elif i.getKind() == RodzajPionka.czarnyzwykly:
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/czarnyzwykły50.jpg)")
                elif i.getKind() == RodzajPionka.bialydama:
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/białadama50.jpg)")
                elif i.getKind() == RodzajPionka.czarnydama:
                    self.goodbuttons[counter].setStyleSheet("background-image: url(assets/czarnadama50.jpg)")
                counter = counter + 1
        self.update()

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
                if (i + j) % 2 == 1 and i >= 0 and i < 3:
                    button.setStyleSheet("background-image: url(assets/białyzwykły50.jpg)")
                    button.setKind(RodzajPionka.bialyzwykly)
                    button.setOwner("player")
                    self.goodbuttons.append(button)
                elif (i + j) % 2 == 1 and i >= 5 and i < 9:
                    button.setStyleSheet("background-image: url(assets/czarnyzwykły50.jpg)")
                    button.setKind(RodzajPionka.czarnyzwykly)
                    button.setOwner("host")
                    self.goodbuttons.append(button)
                elif (i + j) % 2 == 1:
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

    def encodeBoard(self):
        toBeSent = []
        for element in self.goodbuttons:
            toBeSent.append(element.getKind())
        return toBeSent

    def decodeBoard(self, received):
        counter = 0
        for element in received:
            self.goodbuttons[counter].setKind(element)
            if element == RodzajPionka.bialyzwykly or element == RodzajPionka.bialydama:
                self.goodbuttons[counter].setOwner("host")
            elif element == RodzajPionka.czarnyzwykly or element == RodzajPionka.czarnydama:
                self.goodbuttons[counter].setOwner("player")
            else:
                self.goodbuttons[counter].setOwner(None)
            counter = counter + 1
        self.updateboard(self.goodbuttons)
        self.myTurn =True

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    board = Board("host", "player")
    app.exec()
