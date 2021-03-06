
from PySide2 import QtCore, QtWidgets


class Page(QtWidgets.QWidget):
    """ A container and dropevent catcher for widgets """

    def __init__(self, parent, pihud):
        super(Page, self).__init__(parent)
        self.setAcceptDrops(True)
        self.pihud = pihud # normally, this would simply be the parent()
        self.widgets = []
        self.show()


    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        # get relative position of mouse from mimedata
        mime = e.mimeData().text()
        x, y = map(int, mime.split(','))

        e.source().move(e.pos() - QtCore.QPoint(x, y))
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
