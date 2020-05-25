import os
import inspect
import importlib
from PyQt5 import QtWidgets

# the final dict for storing classes by classname

displaywidgets = {}


# find python files in this directory
for f in os.listdir(os.path.dirname(__file__)):
    name, ext = os.path.splitext(f)

    if ext != '.py':
        continue

    if name == '__init__':
        continue

    module = importlib.import_module(name=('.' + name),package='pihud.widgets')

    # search each modules dict for classes that implement QWidget
    for key in module.__dict__:
        e = module.__dict__[key]

        if not inspect.isclass(e):
            continue

        if issubclass(e, QtWidgets.QWidget):
            displaywidgets[key] = e