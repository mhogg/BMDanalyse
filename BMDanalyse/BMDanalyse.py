# -*- coding: utf-8 -*-

# Copyright (C) 2016 Michael Hogg

# This file is part of BMDanalyse - See LICENSE.txt for information on usage and redistribution

import sys
from pyqtgraph.Qt import QtGui
from MainWindow import MainWindow
    
def run():
    # PySide fix: Check if QApplication already exists. Create QApplication if it doesn't exist 
    app = QtGui.QApplication.instance()        
    if not app:
        app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
