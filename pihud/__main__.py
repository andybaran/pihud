
import os
import sys
import obd
import shutil
import serial

from pihud.PiHud import PiHud
from PySide2.QtWidgets import QOpenGLWidget, QApplication
from pihud import GlobalConfig

#Touch
from PySide2.QtCore import Qt, QEvent

config_path         ='/etc/pihud/pihud.json'

def main():
    """ entry point """
    # ============================ Config loading =============================
    
    if os.path.isfile(config_path):
        print("[pihud] using config: ", config_path)
        
    if not os.path.isfile(config_path):
        print("[pihud] Fatal: Missing config file at /etc/pihud/pihud.json")
        sys.exit(1)

    global_config = GlobalConfig.GlobalConfig(config_path)
    
    # =========================== OBD-II Connection ===========================

    if global_config["debug"]:
        obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information

    print('[pihud] OBD2 Port: ', global_config["port"])
    connection = obd.Async(global_config["port"],baudrate=115200,fast=False)

    # =========================== Generic Serial Connection ==================

    # TODO: Create serial connection objects that can be passed to datapollers in pollerHub
    
    # ============================ QT Application =============================
    
    app = QApplication(sys.argv)
    hud = PiHud(global_config, connection)

    # TODO: Hide the cursor for the application that "contains" the hud

    # Enable Touch for the hud
    hud.setAttribute(Qt.WA_AcceptTouchEvents,True)
    #hud.setAttribute(Qt.AA_UseOpenGLES,True)
    hud.installEventFilter(hud)

    # ================================= Start =================================

    status = app.exec_() # blocks until application quit

    # ================================= Exit ==================================

    connection.close()
    sys.exit(status)

if __name__ == "__main__":
    main()
