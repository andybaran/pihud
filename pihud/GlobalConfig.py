import os
import json
from collections import OrderedDict

import obd
from pihud import widgets
from pihud.defaults import default_for

class GlobalConfig():
    """ manages the structure of the config file """

    def __init__(self, filename):
        self.filename = filename
        self.data = OrderedDict([
            ("debug",          False    ),
            ("port",           None     ),
            ("page_adv_pin",   18       ),
            ("color",          "#2e3fcc"),
            ("redline_color",  "#ff0000"),
            ("font_size",      30       ),
            ("note_font_size", 20       ),
            ("pages",          [[]]     ),
        ])
        self.load()


    def make_config(self, command):
        config = default_for(command)
        config.global_config = self
        return config


    def __load_keys(self, src, dest):
        """ copies duplicate keys/values from src to dest dictionaries """
        for key in dest:
            if key in src:
                dest[key] = src[key]


    def load(self):
        """ reads a config from a file """

        file_config = None;

        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                raw_config_json = f.read()
                try:
                    file_config = json.loads(raw_config_json)
                except Exception as e:
                    print("Invalid json in config:")
                    print(str(e))
                    self.filename = "" # prevents save()ing
                    return

        # load the keys/data into the global config
        self.__load_keys(file_config, self.data)

        # output
        pages = []

        for page in self.data['pages']:

            current_page = []

            for widget in page:
                if "sensor" not in widget:
                    print("widget definition missing 'sensor' attribute")
                    break

                originalSensor = widget.get("sensor")
                sensor = originalSensor.upper()
                sensor = sensor.encode('ascii','ignore')
                sensor = sensor.decode()
                print("here")
                if widget.get("datapoller") == 'obd':
                    print("datapoller is obd")
                    config = self.make_config(obd.commands[sensor])
                    # load the keys/data into the global config
                else:
                    config = widget # this can obviously be removed after troubleshooting
                self.__load_keys(widget, config)
                current_page.append(config)
            pages.append(current_page)

        self.data['pages'] = pages

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            raise KeyError("'%s' is not a valid config key" % key)


    def __setitem__(self, key, value):
        if key in self.data:
            self.data[key] = value
        else:
            raise KeyError("'%s' is not a valid config key" % key)


    def __contains__(self, key):
        return key in self.data
