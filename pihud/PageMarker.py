
from PyQt5 import QtWidgets, QtCore, QtGui

class PageMarker(QtWidgets.QWidget):
    def __init__(self, parent):
        super(PageMarker, self).__init__(parent)

        self.height     = 100
        self.bg_color   = QtGui.QColor(255, 255, 255, 50)
        self.fg_color   = QtGui.QColor(255, 255, 255, 70)
        self.screenRect = QtWidgets.QApplication.desktop().screen().rect()

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), self.bg_color)
        self.setPalette(p)

        # make full width, and move to bottom of screen
        self.setFixedWidth(self.screenRect.width())
        self.setFixedHeight(self.height)
        self.move(0, self.screenRect.height() - self.height)

        self.set(1, 0)
        

    def paintEvent(self, e):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(self.marker, self.fg_color)
        painter.end()


    def set(self, n, p):
        inc = self.screenRect.width() / n
        self.marker = QtCore.QRect(inc * p, 0, inc, self.height)
