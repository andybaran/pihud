from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont,QColor,QBrush,QPen,QPainter,QFontDatabase,QPainterPath 
from pihud.util import map_value, in_range, scale, map_scale, map_value, scale_offsets, str_scale
import math


class DigitalBarHorizontal(QWidget):
    def __init__(self, parent, config):
        super(DigitalBarHorizontal, self).__init__(parent)

        self.config = config
        self.value = config["min"]

        self.font      = QFont()
        self.note_font = QFont()
        self.color     = QColor(config["color"])
        self.red_color = QColor(config["redline_color"])
        self.no_color  = QColor()
        self.no_color.setAlpha(0)

        self.brush     = QBrush(self.color)
        self.red_brush = QBrush(self.red_color)

        self.pen       = QPen(self.color)
        self.red_pen   = QPen(self.red_color)
        self.no_pen    = QPen(self.no_color)

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
        self.brush_red_bg = QBrush(QColor("#73311c"))
        self.pen          = QPen(self.pen_color)
        self.red_pen      = QPen(self.red_color)
        self.text_pen     = QPen(self.color)

        self.font.setPixelSize(self.config["font_size"])
        self.note_font.setPixelSize(self.config["note_font_size"])
        self.pen.setWidth(3)
        self.red_pen.setWidth(3)


    def render(self, response):
        # approach the value
        self.value += (response.value.magnitude - self.value) / 4
        self.update()


    def sizeHint(self):
        return QSize(400, 60)


    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)

        self.pre_compute(painter)

        painter.setFont(self.font)
        painter.setPen(self.text_pen)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_title(painter)
        #self.draw_border(painter)
        self.draw_bars(painter)

        painter.end()


    def pre_compute(self, painter):
        w = self.width()
        h = self.height()

        s = scale(self.config["min"], self.config["max"], float(self.config["max"] - self.config["min"])/(self.config["w"]/4))

        self.angles = map_scale(s, 0, self.config["w"])
        self.str_scale, self.multiplier = str_scale(s, self.config["scale_mult"])
        self.red_angle = self.config["w"]
        if self.config["redline"] is not None:
            self.red_angle  = map_value(self.config["redline"], self.config["min"], self.config["max"], 0, self.config["w"])

        # recompute new values
        self.l = 2            # left X value
        self.r = w - self.l # right X value
        self.t_height = self.config["font_size"] + 8
        self.bar_height = max(0, h - self.t_height) - self.l
        self.value_offset = map_value(self.value,
                                        self.config["min"],
                                        self.config["max"],
                                        self.l,
                                        self.r)
        self.red_offset = w
        if self.config["redline"] is not None:
            self.red_offset = map_value(self.config["redline"],
                                          self.config["min"],
                                          self.config["max"],
                                          self.l,
                                          self.r)


    def draw_title(self, painter):
        painter.save()

        r = QRect(0, 0, self.width(), self.t_height)
        painter.drawText(r, Qt.AlignVCenter, self.config["title"])
        #painter.drawText(r, Qt.AlignVCenter, "Test")
        painter.drawRect(r)

        painter.restore()


    def draw_border(self, painter):
        painter.save()
        painter.translate(0, self.t_height)

        if in_range(self.red_offset, self.l, self.r):
            # non-red zone
            path = QPainterPath()
            path.moveTo(self.red_offset, 0)
            path.lineTo(self.l, 0)
            path.lineTo(self.l, self.bar_height)
            path.lineTo(self.red_offset, self.bar_height)

            painter.drawPath(path)

            # red zone
            path = QPainterPath()
            path.moveTo(self.red_offset, 0)
            path.lineTo(self.r, 0)
            path.lineTo(self.r, self.bar_height)
            path.lineTo(self.red_offset, self.bar_height)

            painter.setPen(self.red_pen)
            painter.drawPath(path)

        else:
            painter.drawRect(QRect(
                self.l,
                self.l,
                self.r - self.l,
                self.bar_height,
            ))

        painter.restore()

    def draw_bars(self, painter):
        painter.save()
        painter.translate(0, self.t_height)
        painter.setPen(self.no_pen)
        painter.setBrush(self.brush)

        self.t_height = self.config["font_size"] + 8
        self.bar_height = max(0, self.height() - self.t_height) - self.l
        #end = self.__tick_r - self.__tick_l
        #yTopOffset = int(2 * self.__tick_r * math.sin(math.radians(self.angles[1] / 2)) / 2) #- 1
        #yBottomOffset = int(2 * end * math.sin(math.radians(self.angles[1] / 2)) / 2) #- 1

        angle = map_value(self.value, self.config["min"], self.config["max"], 0, self.config["w"])
        angle = min(angle, self.config["w"])

        for a in self.angles:
            painter.save()
            #painter.rotate(90 + 45 + a)

            if a > self.red_angle and a <= angle:
                painter.setBrush(self.brush_red)
            elif a <= angle:
                painter.setBrush(self.brush)
            elif  a > self.red_angle:
                painter.setBrush(self.brush_red_bg)
            else:
                painter.setBrush(self.brush_bg)

            path = QPainterPath()
            path.moveTo(0, 0 + a)
            path.lineTo(self.bar_height, 0 + a)
            path.lineTo(self.bar_height, 2 + a)
            path.lineTo(0, 2 + a)
            path.lineTo(0, 0 + a)

            painter.drawPath(path)
            painter.restore()

        painter.restore()

    def draw_bar(self, painter):
        painter.save()
        painter.translate(0, self.t_height)
        painter.setPen(self.no_pen)
        painter.setBrush(self.brush)

        if in_range(self.red_offset, self.l, self.r):
            if self.value_offset <= self.red_offset:
                painter.drawRect(QRect(
                    self.l,
                    0,
                    self.value_offset,
                    self.bar_height
                ))
            else:
                painter.drawRect(QRect(
                    self.l,
                    0,
                    self.red_offset,
                    self.bar_height
                ))

                painter.setBrush(self.red_brush)
                painter.setPen(self.red_pen)

                painter.drawRect(QRect(
                    self.red_offset,
                    0,
                    self.value_offset - self.red_offset,
                    self.bar_height
                ))
        else:
            painter.drawRect(QRect(
                    self.l,
                    0,
                    self.value_offset,
                    self.bar_height
            ))

        painter.restore()


class DigitalBarVertical(DigitalBarHorizontal):
    def __init__(self, parent, config):
        super(DigitalBarVertical, self).__init__(parent, config)


    def pre_compute(self, painter):

        painter.rotate(-90)
        painter.translate(-self.height(), 0)

        # swap the X vs Y
        h = self.width()
        w = self.height()

        # recompute new values
        self.l = 2          # left X value
        self.r = w - self.l # right X value
        self.t_height = self.config["font_size"] + 8
        self.bar_height = max(0, h - self.t_height) - self.l
        self.value_offset = map_value(self.value,
                                      self.config["min"],
                                      self.config["max"],
                                      self.l,
                                      self.r)
        self.red_offset = w
        if self.config["redline"] is not None:
            self.red_offset = map_value(self.config["redline"],
                                        self.config["min"],
                                        self.config["max"],
                                        self.l,
                                        self.r)


    def draw_title(self, painter):
        painter.save()

        r = QRect(0, 0, self.height(), self.t_height)
        painter.drawText(r, Qt.AlignVCenter, self.config["title"])

        painter.restore()

