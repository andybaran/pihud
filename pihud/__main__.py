
import os
import sys
import obd
import shutil
from pihud.PiHud import PiHud
from PyQt5 import QtWidgets
from pihud import GlobalConfig

try:
    import RPi.GPIO as GPIO
except:
    print("[pihud] Warning: RPi.GPIO library not found")



# file paths
running_dir         = os.path.dirname(os.path.realpath(__file__))
default_config_path = os.path.join(running_dir, 'default.rc')
config_path         = os.path.join(os.path.expanduser('~'), 'pihud.rc')



def main():
    """ entry point """

    # ============================ Config loading =============================
    if os.path.isfile(config_path):
        print("[pihud] using config: ", config_path)
        
    if not os.path.isfile(config_path):
        # copy the default config
        if not os.path.isfile(default_config_path):
            print("[pihud] Fatal: Missing default config file. Try reinstalling")
            sys.exit(1)
        else:
            shutil.copyfile(default_config_path, config_path)

    global_config = GlobalConfig.GlobalConfig(config_path)
    

    # =========================== OBD-II Connection ===========================

    if global_config["debug"]:
        obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information

    print('[pihud] port: ', global_config["port"])
    connection = obd.Async(global_config["port"])
    

    # if global_config["debug"]:
    #     for i in range(32):
    #         connection.supported_commands.append(obd.commands[1][i])

    # ============================ QT Application =============================

    app = QtWidgets.QApplication(sys.argv)
    hud = PiHud(global_config, connection)

    # ============================== GPIO Setup ===============================

    try:
        pin = self.config.page_adv_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,
                   GPIO.IN,
                   pull_up_down=GPIO.PUD_UP)
        GIO.add_event_detect(pin,
                             GPIO.FALLING,
                             callback=hud.next_page,
                             bouncetime=200)
    except:
        pass

    # ================================= Start =================================

    status = app.exec_() # blocks until application quit

    # ================================= Exit ==================================

    connection.close()
    sys.exit(status)


if __name__ == "__main__":
    main()
