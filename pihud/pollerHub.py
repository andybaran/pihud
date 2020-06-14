# Taken from : https://stackoverflow.com/questions/53445074/using-decorator-arguments-for-switching

#if datatype (from json config) == "custom" call this, otherwise just do the default obd

# setup a place in __main or pihud to have connections already open and waiting to avoid latency

import serial
import struct
import random
import pint

ureg = pint.UnitRegistry()
uart = serial.Serial("/dev/ttyUSB_MEGA1", baudrate=115200)

class sensorvalue:
    def __init__(self):
        self.value = pint

readvalue = sensorvalue()
class pollerHub:
    DEFAULT = "_default"
    def _default(): raise ValueError('Polller function not defined')


    _func_map = {DEFAULT: _default}

    def __init__(self,commandType):
        super().__init__()
        self.commandType = commandType

    def __call__(self, poller_function):
        self._func_map[self.commandType] = poller_function
        return poller_function

    @classmethod
    def poll(cls,commandType):
        return cls._func_map.get(commandType, cls._func_map[cls.DEFAULT])()


@pollerHub('boost')
def _boost():
    r = uart.read_until(size=4)
    if len(r) == 1:
        r = 0 # assume that we're getting passed a null value b/c ambient = boost pressure (common in testing while not hooked up to vehicle)
    else:
        r = struct.unpack('<i',r)
        r = r[0]
        if r > 70:  #in order to avoid 2's complement math gauge code add's 100 to any negative value; -30 is the lowest that can go.
            r = r - 100
    readvalue.value = r * ureg.psi
    return r

@pollerHub('random')
def _random():
    readvalue.value = random.randint(1000,8000) * ureg.psi
    return readvalue