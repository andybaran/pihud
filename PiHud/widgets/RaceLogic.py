
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pihud.util import map_value, in_range
import time

class RaceLogic(QWidget):
    def __init__(self, parent, config):
        super(RaceLogic, self).__init__(parent)

        self.config = config
        self.value = config["min"]

        self.font_db  = QFontDatabase()
        self.font_id  = self.font_db.addApplicationFont("fonts/DS-DIGI.TTF")
        self.families = self.font_db.applicationFontFamilies(self.font_id)
        #print [str(f) for f in self.families] #DS-Digital

        self.font         = QFont("DS-Digital")
        self.title_font   = QFont("DS-Digital")
        self.color        = QColor(config["color"])
        self.red_color    = QColor(config["redline_color"])
        self.pen          = QPen(self.color)
        self.red_pen      = QPen(self.red_color)

        self.start        = 0.0
        self.stop         = 0.0
        self.onetohundred = 0.0

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

        #painter.setRenderHint(QPainter.Antialiasing)

        self.font_size = int(max(self.width()/2, self.height()/2))
        self.title_font_size = int(max(self.width()/8, self.height())/8)
        self.t_height = int(self.height()/3)  # - self.title_font_size * 2

        if len(self.config["title"]) > 0:
            self.draw_title(painter)

        if self.value == 0:
            self.start = time.time()

        if self.value >= self.red_value and self.start > 0:
            self.stop = time.time()
            self.onetohundred = self.stop - self.start
            self.start = 0

        self.draw_value(painter)

        painter.end()

    def draw_value(self, painter):
        painter.save()

        if self.onetohundred > 0:
            painter.setPen(self.red_pen)
        else:
            painter.setPen(self.pen)

        painter.setFont(self.font)
        self.font.setPixelSize(self.font_size)
        r = QRect(0, 0, self.width(), self.t_height*2)
        painter.drawText(r, Qt.AlignCenter|Qt.AlignBottom, "{:.1f}".format(self.onetohundred))
        #painter.drawRect(r)

        painter.restore()

    def draw_title(self, painter):
        painter.save()

        painter.setFont(self.title_font)
        painter.setPen(self.pen)
        self.title_font.setPixelSize(self.title_font_size)
        r = QRect(0, self.t_height*2, self.width(), self.t_height)
        painter.drawText(r, Qt.AlignCenter|Qt.AlignTop, self.config["title"])
        #painter.drawRect(r)

        painter.restore()
