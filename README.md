
This is a fork of a fork of the original [PiHud](https://github.com/brendan-w/pihud). I forked from [this branch](https://github.com/star0x4b/pihud) because it had been recently updated when I started and I like the look of the additional digital gauge types.

Some key differences from the original PiHud:

1. Updated to Python 3.7.3 (probably works with later versions too)
2. Moved from PyQT to PySide2
3. Page switching is done by touching the screen or TAB key; *I've tested with the official RPI Display*
4. Custom data sources are available using the pollerHub class; *An [arduino boost gauge](https://github.com/andybaran/mega-boostgauge) for example*
5. Removed ability to add widgets while running; driving is distracting enough.
 

Turning your Pi into a PiHud
----------------------------

For installation on Raspbian git clone and run pihud-installer.sh.  This simple script will install python3, as many python packages as possible via apt, remaining packages via pip and setup PiHud to run on boot using systemd.

Configuring
-----------

PiHud is configured by modifying a file named `pihud.json` in /etc/pihud/pihud.json

-   The `sensor` field is the string name for any sensor your car supports. A full list can be found in the [python-OBD wiki](http://python-obd.readthedocs.io/en/latest/Command%20Tables/)
-   The `type` field selects the way data is displayed. Values correspond with any class in the [widgets folder](https://github.com/andybaran/pihud/tree/master/pihud/widgets).
-   All color attributes accept CSS color values
-   The `demo` key is used to feed a sin() curve into all widgets for testing.
-   The `debug` key is used to turn python-OBD's debug printing on and off. If enabled, you will see OBD debug information being printed to `stderr`.
-   The `datapoller` field corresponds to a function in [pollerHub.py](https://github.com/andybaran/pihud/blob/master/pihud/pollerHub.py) and allows for displaying data from sources other than OBD.  
