import os
import inspect
import importlib
from PyQt5 import QtWidgets

# the final dict for storing classes by classname
widgets = {}

# find python files in this directory
for f in os.listdir(os.path.dirname(__file__)):
    name, ext = os.path.splitext(f)

    if ext != '.py':
        continue

    if name == '__init__':
        continue

    print("Name = " + name)
    print("Ext = " + ext)
    
    # import the module (old school)
    # module = __import__(name, locals(), globals())

    module = importlib.import_module(name=(name))

    print("module = " + module)

    # search each modules dict for classes that implement QWidget
    for key in module.__dict__:
        e = module.__dict__[key]

        if not inspect.isclass(e):
            continue

        if issubclass(e, QtWidgets.QWidget):
            widgets[key] = e