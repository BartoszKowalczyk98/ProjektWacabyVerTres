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
        self.playername = 'Gracz1'
        self.opponent = 'Gracz2'
        self.status = self.statusBar()
        self.initUI()

    def uncheckall(self):
        for i in range(0, 8):
            self.grupy[i].setExclusive(False)
            for j in range(1, 9):
                self.grupy[i].button(j).setChecked(False)
            self.grupy[i].setExclusive(True)

    def buttonpressed(self):
        # print("Czy bicie jest dostepne?", self.isBeatingPossible("Gracz1"))
        for i in range(0, 8):
            self.tempbutton = self.grupy[i].checkedButton()
            tempint = (i, self.grupy[i].checkedId())
            if self.tempbutton is not None:
                break
        self.changeColor(1)
        self.uncheckall()
        self.checkMove(tempint)

    def isBeatingPossible(self, user):
        self.status.showMessage('Jest możliwość bicia')
        for i in range(0, 8):
            for j in range(0, 8):
                if self.goodbuttons[i * 8 + j].getOwner() == user:
                    if i - 2 >= 0 and j - 2 >= 0 and self.goodbuttons[(i - 1) * 8 + (j - 1)].getOwner() != user and \
                            self.goodbuttons[(i - 1) * 8 + (j - 1)].getOwner() is not None and self.goodbuttons[(i - 2) * 8 + j - 2].getKind() == RodzajPionka.pusty:
                        self.goodbuttons[(i - 2) * 8 + j - 2].setStyleSheet("background-color: aqua")
                        return True
                    elif i - 2 >= 0 and j + 2 <= 7 and self.goodbuttons[(i - 1) * 8 + (j + 1)].getOwner() != user and \
                            self.goodbuttons[(i - 1) * 8 + (j + 1)].getOwner() is not None and self.goodbuttons[(i - 2) * 8 + j + 2].getKind() == RodzajPionka.pusty:
                        self.goodbuttons[(i - 2) * 8 + j + 2].setStyleSheet("background-color: aqua")
                        return True
                    elif i + 2 <= 7 and j - 2 >= 0 and self.goodbuttons[(i + 1) * 8 + (j - 1)].getOwner() != user and \
                            self.goodbuttons[(i + 1) * 8 + (j - 1)].getOwner() is not None and self.goodbuttons[(i + 2) * 8 + j - 2].getKind() == RodzajPionka.pusty:
                        self.goodbuttons[(i + 2) * 8 + j - 2].setStyleSheet("background-color: aqua")
                        return True
                    elif i + 2 <= 7 and j + 2 <= 7 and self.goodbuttons[(i + 1) * 8 + (j + 1)].getOwner() != user and \
                            self.goodbuttons[(i + 1) * 8 + (j + 1)].getOwner() is not None and self.goodbuttons[(i + 2) * 8 + j + 2].getKind() == RodzajPionka.pusty:
                        self.goodbuttons[(i + 2) * 8 + j + 2].setStyleSheet("background-color: aqua")
                        return True
        self.status.showMessage('Normalny ruch')
        return False

    def checkMove(self, tempint):
        doIHaveToBeat = self.isBeatingPossible(self.playername)  # musi byc nazwa gracza jakąś zmienną
        if self.lastclicked == tempint:  # odklikanie
            print("odklikanie")
            self.lastclicked = ()
        elif self.lastclicked != ():  # ruch
            if doIHaveToBeat:
                completed = self.beatingMove(tempint, self.playername, self.opponent)
            else:
                completed = self.noBeatingMove(tempint)
            if not completed:
                return
        else:  # zaznaczenie co chcemy przesunąć
            if self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].getKind() == RodzajPionka.pusty:
                self.lastclicked = ()
            elif self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].getOwner() != self.playername:
                self.lastclicked = ()
            else:
                print("kliknieto: ", tempint)
                self.lastclicked = tempint

    def beatingMove(self, tempint, owner, opponent):
        wektorPrzeskoku = (tempint[0] - self.lastclicked[0], tempint[1] - self.lastclicked[1])
        if abs(wektorPrzeskoku[1]) != 2 or abs(wektorPrzeskoku[0]) != 2:
            return False
        if self.goodbuttons[tempint[0] * 8 + tempint[1] - 1].getKind() != RodzajPionka.pusty:
            return False
        if self.goodbuttons[(self.lastclicked[0] + int(wektorPrzeskoku[0] / 2)) * 8 + (
                self.lastclicked[1] + int(wektorPrzeskoku[1] / 2) - 1)].getOwner() != opponent:
            return False
        print("ruch z : ", self.lastclicked, " na ", tempint)
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
                    button.setOwner("Gracz1")
                    self.goodbuttons.append(button)
                elif (i + j) % 2 == 1 and i >= 5 and i < 9:
                    button.setStyleSheet("background-image: url(assets/czarnyzwykły50.jpg)")
                    button.setKind(RodzajPionka.czarnyzwykly)
                    button.setOwner("Gracz2")
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


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    board = Board()
    sys.exit(app.exec())
