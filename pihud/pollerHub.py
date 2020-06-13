# Taken from : https://stackoverflow.com/questions/53445074/using-decorator-arguments-for-switching

#if datatype (from json config) == "custom" call this, otherwise just do the default obd

# setup a place in __main or pihud to have connections already open and waiting to avoid latency

import serial
import random

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
       cls._func_map.get(commandType, cls._func_map[cls.DEFAULT])()

@pollerHub('boost')
def _boost():
    uart = serial.Serial("/dev/ttyUSB_MEGA1", baudrate=115200)
    r = self.uart.read_until(size=4)
    if len(r) == 1:
        r = 0 # assume that we're getting passed a null value b/c ambient = boost pressure (common in testing while not hooked up to vehicle)
    else:
        r = struct.unpack('<i',r)
        r = r[0]
    return r

@pollerHub('random')
def _random():
    r = random.randint(1000,8000)
    print(r)
    return r