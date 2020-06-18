
from pihud.Page import Page
from pihud.pollerHub import pollerHub, sensorvalue
from pihud.Widget import Widget
from PySide2 import QtWidgets, QtCore, QtGui

#Touch events
from PySide2.QtCore import QEvent
from PySide2.QtCore import Qt

class PiHud(QtWidgets.QMainWindow):
    def __init__(self, global_config, connection):
        super(PiHud, self).__init__()

        self.global_config = global_config
        self.connection = connection

        # ================= Color Palette =================

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(palette)

        # ================== Init Pages ===================

        self.stack      = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # read the config and make pages
        for configs in global_config["pages"]:
            self.__add_existing_page(configs)

        # ===================== Start =====================
        
        self.timer = QtCore.QBasicTimer()
        self.setWindowTitle("PiHud")
        self.showFullScreen()

        self.start()

    def __page(self):
        return self.stack.currentWidget()

    def __index(self):
        return self.stack.currentIndex()

    def __count(self):
        return self.stack.count()

    # def __save(self):
    #     pages = []

    #     for i in range(self.__count()):
    #         page = self.stack.widget(i)
    #         current_page = []
    #         for widget in page.widgets:
    #             current_page.append(widget.config)
    #         pages.append(current_page)

    #     self.global_config.save(pages)

    # ========= Main loop =========

    def timerEvent(self, event):
        page = self.__page()

        for widget in page.widgets:
            if widget.config['datapoller'] == "obd":
                widget.render(self.connection.query(widget.get_command()))
            else :
                r = widget.get_command()
                widget.render(r)


    def start(self):
        # watch the commands on this page
        for widget in self.__page().widgets:
            if widget.config['datapoller'] == "obd":
                self.connection.watch(widget.get_command())
        self.connection.start()
        self.timer.start(1000/30, self) #this defines the refresh value in milliseconds...3 times per second seems reasonable


    def stop(self):
        self.timer.stop()
        self.connection.stop()
        self.connection.unwatch_all()


    def restart(self):
        self.stop()
        self.start()

    # ========= Page Actions =========

    def __add_existing_page(self, configs=None):
        page = Page(self.stack, self)

        if configs is not None:
            for config in configs:
                self.__add_existing_widget(page, config)

        self.stack.addWidget(page)
    
    def goto_page(self, p):
        p = p % self.stack.count()

        self.stop()

        # switch page
        self.stack.setCurrentIndex(p)

        self.start()

    def next_page(self):
        self.goto_page(self.__index() + 1)
 
    # ========= Widget Actions =========

    def __add_existing_widget(self, page, config):
        # make a widget from the given config
        thiswidget = Widget(page, config)

        # add it to the page
        page.widgets.append(thiswidget)

    def keyPressEvent(self, e):
        key = e.key()

        if key == QtCore.Qt.Key_Escape:
            self.stop()
            self.close()

        elif key == QtCore.Qt.Key_Tab:
            self.next_page()

    # Handle touch events
    def eventFilter(self, obj, event):
        if event.type() == QEvent.TouchBegin:
            self.next_page()
            return True
        elif event.type() == QEvent.TouchEnd:
            return True 
        return super(PiHud, self).eventFilter(obj,event)

    def closeEvent(self, e):
        quit()
