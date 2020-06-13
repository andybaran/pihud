import obd
from pihud import PiHud
from pihud.pollerHub import pollerHub, sensorvalue
from pihud.widgets import displaywidgets
from PyQt5 import QtCore, QtWidgets

class Widget(QtWidgets.QWidget):

    def __init__(self, parent, config):
        super(Widget, self).__init__(parent)
        self.config = config
        print("widget init config : ", config)

        '''TODO : make this work with QML multitouch two finger touch'''
        self.menu = QtWidgets.QMenu()
        self.menu.addAction(self.config["sensor"]).setDisabled(True)

        subMenu = self.menu.addMenu("Widget Type")
        for w in displaywidgets:
            a = subMenu.addAction(w)
            a.setData(displaywidgets[w])

        self.menu.addAction("Delete Widget", self.delete)
    
        # instantiate the requested graphics object
        print("from widget.py", config)
        self.graphics = displaywidgets[config["type"]](self, config)

        self.move(self.position())
        self.show()


    def sizeHint(self):
        if (self.config['w'] is not None) and \
           (self.config['h'] is not None):
            size = QtCore.QSize(self.config['w'], self.config['h'])
            self.graphics.setFixedSize(size)
            return size
        else:
            s = self.graphics.sizeHint()
            self.config['w'] = s.width()
            self.config['h'] = s.height()
            return s


    def position(self):
        return QtCore.QPoint(self.config['x'], self.config['y'])


    def moveEvent(self, e):
        pos = e.pos()
        self.config['x'] = pos.x()
        self.config['y'] = pos.y()


    def delete(self):
        self.parent().delete_widget(self)


    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:

            mimeData = QtCore.QMimeData()
            mimeData.setText('%d,%d' % (e.x(), e.y()))

            # show the ghost image while dragging
            pixmap = QtWidgets.QPixmap.grabWidget(self)
            painter = QtWidgets.QPainter(pixmap)
            painter.fillRect(pixmap.rect(), QtWidgets.QColor(0, 0, 0, 127))
            painter.end()

            drag = QtWidgets.QDrag(self)
            drag.setMimeData(mimeData)
            drag.setPixmap(pixmap)
            drag.setHotSpot(e.pos())

            drag.exec_(QtCore.Qt.MoveAction)


    def contextMenuEvent(self, e):
        action = self.menu.exec_(self.mapToGlobal(e.pos()))
    
    
    def get_command(self):
        if self.config['datapoller'] == 'obd':
            s = self.config["sensor"]
            if s in obd.commands:
                return obd.commands[s]
            else:
                raise KeyError("'%s' is not a valid OBDCommand" % s)
        else:
            pollvalue = pollerHub.poll(self.config['datapoller'])
            print("pollvalue ", pollvalue)
            return pollvalue

    def render(self, response):
        # we might grab an INT from a CLI command, serial, etc. which could be equal to 0 (null)
        print("poll response is: ", response)
        if isinstance(response, int):
            self.graphics.render(response)
            return     

        # TODO - There has to be a better way to handle this is_null doesn't work with pint ints
        #if not response.is_null():
        self.graphics.render(response)
