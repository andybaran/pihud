
import os
import sys
import obd
import shutil
from pihud.PiHud import PiHud
from PyQt5 import QtWidgets
from pihud import GlobalConfig

#Touch
from PyQt5.QtCore import Qt, QEvent

config_path         ='/etc/pihud/pihud.rc'

def main():
    """ entry point """

    # ============================ Config loading =============================
    
    if os.path.isfile(config_path):
        print("[pihud] using config: ", config_path)
        
    if not os.path.isfile(config_path):
        print("[pihud] Fatal: Missing default config file. Try reinstalling")
        sys.exit(1)

    global_config = GlobalConfig.GlobalConfig(config_path)
    

    # =========================== OBD-II Connection ===========================

    if global_config["debug"]:
        obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information

    print('[pihud] OBD2 Port: ', global_config["port"])
    connection = obd.Async(global_config["port"],baudrate=115200)

    # ============================ QT Application =============================
    
    app = QtWidgets.QApplication(sys.argv)
    hud = PiHud(global_config, connection)
    
    # Hide the cursor for the application that "contains" the hud
    # TODO: figure out how to do this 

    # Enable Touch for the hud
    hud.setAttribute(Qt.WA_AcceptTouchEvents,True)
    hud.installEventFilter(hud)

    # ================================= Start =================================

    status = app.exec_() # blocks until application quit

    # ================================= Exit ==================================

    connection.close()
    sys.exit(status)

if __name__ == "__main__":
    main()