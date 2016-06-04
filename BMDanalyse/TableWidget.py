# -*- coding: utf-8 -*-

# Copyright (C) 2013 Michael Hogg

# This file is part of BMDanalyse - See LICENSE.txt for information on usage and redistribution

from pyqtgraph.Qt import QtCore,QtGui

class TableWidget(QtGui.QTableWidget):
    
    def __init__(self, x, y, parent = None):
        super(TableWidget, self).__init__(x, y, parent)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.itemChanged.connect(self.tableItemChanged)
        self.currentItemChanged.connect(self.tableUpdateItemText)
        self.currentItemText = None
        
        self.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        hh = self.horizontalHeader()
        hh.setDefaultSectionSize(125)
        vh = self.verticalHeader()
        vh.setDefaultSectionSize(25) 
        
    def tableUpdateItemText(self,itemCurr,itemPrev):
        self.currentItemText = itemCurr.text()
        
    def tableItemChanged(self,item):
        self.errorMessage = QtGui.QMessageBox()
        try: 
            itemValue = float(item.text())
        except: 
            if self.currentItemText!=None: item.setText(self.currentItemText)
            icon = self.parent().windowIcon()
            self.errorMessage.setWindowIcon(icon)
            self.errorMessage.setWindowTitle('BMDanalyse')
            self.errorMessage.setText('Input error: Value must be a number')
            self.errorMessage.setIcon(QtGui.QMessageBox.Warning)           
            self.errorMessage.open()            
        else:
            item.setText('%.2f' % itemValue)
            self.currentItemText = item.text()
       
    def sizeHint(self):
        margins = self.contentsMargins()
        hh      = self.horizontalHeader()
        vh      = self.verticalHeader()
        hsb     = self.horizontalScrollBar()
        vsb     = self.verticalScrollBar()
        vsb.setMaximumWidth(17)
        hsb.setMaximumHeight(17)
        numCols, numRows = (2,15)
        width  = numCols * hh.defaultSectionSize() + margins.left() + margins.right()  + vh.width()  + vsb.width()
        height = numRows * vh.defaultSectionSize() + margins.top()  + margins.bottom() + hh.height() + hsb.height()
        return QtCore.QSize(width, height)