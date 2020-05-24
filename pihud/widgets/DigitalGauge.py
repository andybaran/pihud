from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont,QColor,QBrush,QPen,QPainter,QFontDatabase,QPainterPath 
from pihud.util import scale, map_scale, map_value, scale_offsets, str_scale
import math

class DigitalGauge(QWidget):
    def __init__(self, parent, config):
        super(DigitalGauge, self).__init__(parent)

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
        self.brush_bg     = QBrush(QColor("#555555"))
        self.brush_red    = QBrush(self.red_color)
        self.brush_red_bg = QBrush(self.red_color)
        self.pen          = QPen(self.pen_color)
        self.red_pen      = QPen(self.red_color)
        self.text_pen     = QPen(self.color)

        self.font.setPixelSize(self.config["font_size"])
        
        self.pen.setWidth(1)
        self.red_pen.setWidth(1)
        
        # TODO: make 80 configurable
        s = scale(config["min"], config["max"], float(config["max"] - config["min"])/80)

        self.angles = map_scale(s, 0, 270)
        self.str_scale, self.multiplier = str_scale(s, config["scale_mult"])

        self.red_angle = 270
        if config["redline"] is not None:
            self.red_angle  = map_value(config["redline"], config["min"], config["max"], 0, 270)


    def render(self, response):
        # approach the value
        self.value += (response.value.magnitude - self.value) / 8
        self.update()


    def sizeHint(self):
        return QSize(350, 300)


    def paintEvent(self, e):

        r = min(self.width(), self.height()) / 2
        self.__text_r   = r - (r/10)   # radius of the text
        self.__tick_r   = r - (r/8)    # outer radius of the tick marks
        self.__tick_l   = (r/6)       # length of each tick, extending inwards
        self.__needle_l = (r/5) * 3    # length of the needle

        self.font.setPixelSize(int(max(self.width(), self.height())/3))
        self.note_font.setPixelSize(int(max(self.width(), self.height())/30))
        self.title_font.setPixelSize(int(max(self.width(), self.height())/12))

        painter = QPainter()
        painter.begin(self)

        painter.setFont(self.font)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_title(painter)
        self.draw_value(painter)
        if self.config["numerals"]:
            self.draw_multiplier(painter)
        self.draw_marks(painter)

        painter.end()


    def draw_marks(self, painter):
        painter.save()

        painter.translate(self.width() / 2, self.height() / 2)

        # draw the ticks

        end = self.__tick_r - self.__tick_l
        yTopOffset = int(2 * self.__tick_r * math.sin(math.radians(self.angles[1] / 2)) / 2) #- 1
        yBottomOffset = int(2 * end * math.sin(math.radians(self.angles[1] / 2)) / 2) #- 1

        angle = map_value(self.value, self.config["min"], self.config["max"], 0, 270)
        angle = min(angle, 270)

        for a in self.angles:
            painter.save()
            painter.rotate(90 + 45 + a)

            if a > self.red_angle and a <= angle:
                painter.setBrush(self.brush_red)
            elif a <= angle:
                painter.setBrush(self.brush)
            elif  a > self.red_angle:
                painter.setBrush(self.brush_red_bg)
            else:
                painter.setBrush(self.brush_bg)

            path = QPainterPath()
            path.moveTo(end, -yBottomOffset)
            path.lineTo(self.__tick_r, -yTopOffset)
            path.lineTo(self.__tick_r, yTopOffset)
            path.lineTo(end, yBottomOffset)
            path.lineTo(end, -yBottomOffset)

            painter.drawPath(path)

            painter.restore()
        painter.restore()

    def draw_title(self, painter):
        painter.save()
        painter.setPen(self.text_pen)
        painter.setFont(self.title_font)

        font_offset = int(self.height()/8)

        r_height = self.config["font_size"] + font_offset
        r = QRect(0, self.height() - r_height, self.width(), r_height)
        painter.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, self.config["title"])

        painter.restore()

    def draw_value(self, painter):
        painter.save()
        painter.setPen(self.text_pen)
        painter.setFont(self.font)

        r_height = self.height()/2 + 20
        #r = QRect(0, self.height()/2 - r_height/2, self.width(), self.height()/2 + r_height/2)
        r = QRect(0, 0, self.width(), self.height())
        painter.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(int(self.value//self.multiplier)))
        #painter.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, "TEST")

        painter.restore()

    def draw_multiplier(self, painter):
        if self.multiplier > 1:
            painter.save()

            painter.setPen(self.text_pen)
            painter.setFont(self.note_font)
            s = "x" + str(self.multiplier)
            r = QRect(0, self.width() / 6, self.width(), self.height())
            painter.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, s)

            painter.restore()
