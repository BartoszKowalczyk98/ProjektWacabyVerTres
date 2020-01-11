from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MyPushButton(QPushButton):
    def __init__(self, kind, owner = None, parent = None):
        super(MyPushButton,self).__init__(parent)
        self.kind = kind
        self.owner = owner

    def setKind(self, kind):
        self.kind = kind

    def getKind(self):
        return self.kind

    def setOwner(self, owner):
        self.owner = owner

    def getOwner(self):
        return self.owner

    def getSelf(self):
        return self