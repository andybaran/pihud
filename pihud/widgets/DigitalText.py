
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
        self.note_font    = QFont("DS-Digital")
        self.title_font   = QFont("DS-Digital")
        self.color        = QColor(config["color"])
        self.pen_color    = QColor(Qt.black)
        self.red_color    = QColor(config["redline_color"])
        self.brush        = QBrush(self.color)
        self.brush_bg     = QBrush(QColor("#222222"))
        self.brush_red    = QBrush(self.red_color)
        self.brush_red_bg = QBrush(QColor("#332222"))
        self.pen          = QPen(self.pen_color)
        self.red_pen      = QPen(self.red_color)
        self.text_pen     = QPen(self.color)

        #self.font.setPixelSize(self.config["font_size"])
        self.font.setPixelSize(int(max(self.width(), self.height())/1.5))
        self.note_font.setPixelSize(int(max(self.width(), self.height())/10))
        self.title_font.setPixelSize(int(max(self.width(), self.height())/7))

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

        self.t_height = self.config["font_size"] + 8

        painter.setFont(self.font)
        painter.setPen(self.pen)
        painter.setRenderHint(QPainter.Antialiasing)

        h = 0

        if len(self.config["title"]) > 0:
            h += self.t_height
            r = QRect(0, 0, self.width(), self.t_height)
            painter.drawText(r, Qt.AlignVCenter, self.config["title"])

        r = QRect(0, h, self.width(), self.t_height)
        painter.drawText(r, Qt.AlignCenter, str(int(round(self.value))))

        painter.end()
