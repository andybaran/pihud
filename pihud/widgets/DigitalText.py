
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pihud.util import map_value, in_range


class DigitalText(QWidget):
    def __init__(self, parent, config):
        super(DigitalText, self).__init__(parent)

        self.config = config
        self.value = config["min"]

        self.font_db  = QFontDatabase()
        self.font_id  = self.font_db.addApplicationFont("fonts/DS-DIGI.TTF")
        self.families = self.font_db.applicationFontFamilies(self.font_id)
        #print [str(f) for f in self.families] #DS-Digital

        self.font         = QFont("DS-Digital")
        self.color        = QColor(config["color"])
        self.red_color    = QColor(config["redline_color"])
        self.pen          = QPen(self.color)

        self.red_value = config["redline"]
        if self.red_value is None:
            self.red_value = config["max"]

    def sizeHint(self):
        return QSize(300, 75)


    def render(self, response):
        self.value = response.value.magnitude
        self.update()


    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)

        self.font_size = int(max(self.width(), self.height())/2)
        self.title_font_size = int(self.font_size/3)
        self.t_height = self.height() - self.title_font_size*2

        painter.setFont(self.font)
        painter.setPen(self.pen)
        #painter.setRenderHint(QPainter.Antialiasing)

        if len(self.config["title"]) > 0:
            #self.font.setPixelSize(self.title_font_size)
            self.font.setPixelSize(50)
            r = QRect(0, self.t_height + 1, self.width() - 1, self.height() - self.t_height - 10)
            painter.drawText(r, Qt.AlignCenter, self.config["title"])

        self.font.setPixelSize(self.font_size)
        r = QRect(0, 0, self.width(), self.t_height)
        painter.drawText(r, Qt.AlignCenter, str(int(round(self.value))))

        painter.end()
