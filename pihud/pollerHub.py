# Taken from : https://stackoverflow.com/questions/53445074/using-decorator-arguments-for-switching

#if datatype (from json config) == "custom" call this, otherwise just do the default obd

# setup a place in __main or pihud to have connections already open and waiting to avoid latency

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

@pollerHub('obd')
def _obd():
    print("mmmm...OBD")

@pollerHub('boost')
def _boost():
    print("SONIC BOOM!")

@pollerHub('uart')
def _uart():
    print("more serial data")

def getcommand(obdcommand):
    obdcommand = obdcommand
    pollerHub.poll(obdcommand)

getcommand('boost')
getcommand('obd')
getcommand('uart')
#getcommand('smoke signals')