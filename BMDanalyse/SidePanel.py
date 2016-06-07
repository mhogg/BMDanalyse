# -*- coding: utf-8 -*-

# Copyright (C) 2016 Michael Hogg

# This file is part of BMDanalyse - See LICENSE.txt for information on usage and redistribution

from pyqtgraph.Qt import QtCore,QtGui
        
class SidePanel(QtGui.QWidget):

    def __init__(self, parent=None):
    
        QtGui.QWidget.__init__(self,parent)
        
        self.setMinimumWidth(250)
        self.buttMinimumSize = QtCore.QSize(36,36)
        self.iconSize        = QtCore.QSize(24,24)         
        self.icons           = self.parent().icons

        self.setupImageToolbox()
        self.setupRoiToolbox()
        self.setupAnalysisToolbox()

        sidePanelLayout = QtGui.QVBoxLayout()
        sidePanelLayout.addWidget(self.imageToolbox)
        sidePanelLayout.addWidget(self.roiToolbox)
        sidePanelLayout.addWidget(self.analysisToolbox)
        sidePanelLayout.setContentsMargins(0,0,0,0)
        self.setLayout(sidePanelLayout)
        
    def setupImageToolbox(self):
    
        # Image filelist
        imageFileListLabel = QtGui.QLabel("Image toolbox")
        imageFileListLabel.setContentsMargins(0,0,0,5)
        self.imageFileList = QtGui.QListWidget() 
        self.imageFileList.setToolTip("List of image files")
        # Image buttons
        self.buttImageAdd  = QtGui.QPushButton(self.icons['imageAddIcon'],"")
        self.buttImageRem  = QtGui.QPushButton(self.icons['imageRemIcon'],"")
        self.buttImageUp   = QtGui.QPushButton(self.icons['imageUpIcon'],"")
        self.buttImageDown = QtGui.QPushButton(self.icons['imageDownIcon'],"")
        imageButtons       = [self.buttImageAdd,self.buttImageRem,self.buttImageUp,self.buttImageDown]
        imageToolTips      = ['Add image(s)','Remove selected image','Move image down','Move image up']
        for i in xrange(len(imageButtons)): 
            image = imageButtons[i]
            image.setMinimumSize(self.buttMinimumSize)
            image.setIconSize(self.iconSize)
            image.setToolTip(imageToolTips[i])  
        self.imageFileTools  = QtGui.QFrame()
        imageFileToolsLayout = QtGui.QHBoxLayout() 
        self.imageFileTools.setLayout(imageFileToolsLayout) 
        self.imageFileTools.setContentsMargins(0,0,0,0)
        imageFileToolsLayout.setContentsMargins(0,5,0,0)
        imageFileToolsLayout.addWidget(self.buttImageAdd)
        imageFileToolsLayout.addWidget(self.buttImageRem)        
        imageFileToolsLayout.addWidget(self.buttImageDown)
        imageFileToolsLayout.addWidget(self.buttImageUp)
        # Image Toolbox (containing imageFileList + imageFileList buttons)
        self.imageToolbox = QtGui.QFrame()
        self.imageToolbox.setLineWidth(2)
        self.imageToolbox.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        imageToolboxLayout = QtGui.QVBoxLayout()
        self.imageToolbox.setLayout(imageToolboxLayout)       
        imageToolboxLayout.addWidget(imageFileListLabel)
        imageToolboxLayout.addWidget(self.imageFileList)         
        imageToolboxLayout.addWidget(self.imageFileTools)
    
    def createRoiMenu(self):
        self.roiMenu = popupMenu(self, self.buttRoiAdd)        

    def showRoiMenu(self):
        if self.roiMenu==None:
            self.createRoiMenu()
        self.roiMenu.update()
        self.roiMenu.show()        

    def setupRoiToolbox(self):   
        # ROI buttons
        roitoolboxLabel = QtGui.QLabel("ROI toolbox")
        self.buttRoiAdd  = QtGui.QPushButton(self.icons['roiAddIcon'],"")
        self.buttRoiRem  = QtGui.QPushButton(self.icons['roiRemIcon'],"")
        self.buttRoiSave = QtGui.QPushButton(self.icons['roiSaveIcon'],"")
        self.buttRoiCopy = QtGui.QPushButton(self.icons['roiCopyIcon'],"")        
        self.buttRoiLoad = QtGui.QPushButton(self.icons['roiLoadIcon'],"")
        roiButtons       = [self.buttRoiAdd, self.buttRoiRem,self.buttRoiSave,self.buttRoiCopy,self.buttRoiLoad]
        roiToolTips      = ['Add ROI','Delete ROI','Save ROI','Copy ROI','Load ROI']
        for i in xrange(len(roiButtons)): 
            button = roiButtons[i]
            button.setMinimumSize(self.buttMinimumSize)
            button.setIconSize(self.iconSize)
            button.setToolTip(roiToolTips[i])
        # Connect buttRoiAdd button to a popup menu to select roi type
        self.createRoiMenu()        
        self.buttRoiAdd.clicked.connect(self.showRoiMenu)      
        # ROI Buttons Frame       
        self.roiButtonsFrame = QtGui.QFrame()
        roiButtonsLayout     = QtGui.QHBoxLayout()
        self.roiButtonsFrame.setLayout(roiButtonsLayout)
        self.roiButtonsFrame.setContentsMargins(0,0,0,0)
        roiButtonsLayout.setContentsMargins(0,5,0,0)
        roiButtonsLayout.addWidget(self.buttRoiAdd)
        roiButtonsLayout.addWidget(self.buttRoiLoad) 
        roiButtonsLayout.addWidget(self.buttRoiCopy)
        roiButtonsLayout.addWidget(self.buttRoiSave)
        roiButtonsLayout.addWidget(self.buttRoiRem)
        # ROI Toolbox
        self.roiToolbox  = QtGui.QFrame()
        roiToolboxLayout = QtGui.QVBoxLayout()
        self.roiToolbox.setLayout(roiToolboxLayout)
        self.roiToolbox.setLineWidth(2)
        self.roiToolbox.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)  
        roiToolboxLayout.addWidget(roitoolboxLabel)
        roiToolboxLayout.addWidget(self.roiButtonsFrame)
        
    def setupAnalysisToolbox(self):
        # Analysis buttons
        analysistoolboxLabel = QtGui.QLabel("Analysis toolbox")
        self.buttRoiAnalysis  = QtGui.QPushButton("ROI Analysis")
        self.buttImgAnalysis  = QtGui.QPushButton("Image Analysis")
        self.buttRoiAnalysis.setMinimumSize(self.buttMinimumSize)
        self.buttImgAnalysis.setMinimumSize(self.buttMinimumSize)  
        self.buttRoiAnalysis.setToolTip("Run ROI analysis")
        self.buttImgAnalysis.setToolTip("Run Image analysis")
        # Analysis Buttons Frame       
        self.analysisButtonsFrame = QtGui.QFrame()
        analysisButtonsLayout     = QtGui.QHBoxLayout()
        self.analysisButtonsFrame.setLayout(analysisButtonsLayout)
        self.analysisButtonsFrame.setContentsMargins(0,0,0,0)
        analysisButtonsLayout.setContentsMargins(0,5,0,0)
        analysisButtonsLayout.addWidget(self.buttRoiAnalysis)
        analysisButtonsLayout.addWidget(self.buttImgAnalysis) 
        # Analysis Toolbox
        self.analysisToolbox  = QtGui.QFrame()
        analysisToolboxLayout = QtGui.QVBoxLayout()
        self.analysisToolbox.setLayout(analysisToolboxLayout)
        self.analysisToolbox.setLineWidth(2)
        self.analysisToolbox.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)  
        analysisToolboxLayout.addWidget(analysistoolboxLabel)
        analysisToolboxLayout.addWidget(self.analysisButtonsFrame)
      
    def addImageToList(self,filename):
        self.imageFileList.addItem(filename) 

    def moveImageUp(self):
        """ Move current item up the list """
        # Get current row
        currentRow = self.imageFileList.currentRow()
        # If no row is current, set first row as current
        if currentRow==-1: 
            self.imageFileList.setCurrentRow(0)
            currentRow = self.imageFileList.currentRow()
        # Do not move up list if already at the end
        if (currentRow+1) <= self.imageFileList.count()-1: 
            item = self.imageFileList.currentItem()
            self.imageFileList.takeItem(currentRow)
            self.imageFileList.insertItem(currentRow+1,item.text())
            self.imageFileList.setCurrentRow(currentRow+1)
        # Show current item as selected
        currentItem = self.imageFileList.currentItem()  
        if not currentItem is None: 
            currentItem.setSelected(True)
        
    def moveImageDown(self):
        """ Move current item down the list """ 
        # Get current row
        currentRow = self.imageFileList.currentRow()
        # If no row is current, set first row as current        
        if currentRow==-1: 
            self.imageFileList.setCurrentRow(0)  
            currentRow = self.imageFileList.currentRow()  
        # Do not move down list if already at the beginning    
        if (currentRow-1) >= 0:
            item = self.imageFileList.currentItem()
            self.imageFileList.takeItem(currentRow)
            self.imageFileList.insertItem(currentRow-1,item.text())
            self.imageFileList.setCurrentRow(currentRow-1)
        # Show current item as selected            
        currentItem = self.imageFileList.currentItem() 
        if not currentItem is None: 
            currentItem.setSelected(True)

    def getListOfImages(self):
        """ Create a list of all items in the listWidget """
        items = []
        for index in xrange(self.imageFileList.count()):
            items.append(self.imageFileList.item(index))        
        return items
        
    def updateRoiInfoBox(self,name="",pos="",size="",angle=""):
        self.roiNameValue.setText(name)
        self.roiPosValue.setText(pos)
        self.roiSizeValue.setText(size)
        self.roiAngleValue.setText(angle)
        
class popupMenu(QtGui.QWidget):

    def __init__(self, parent = None, widget=None): 
        QtGui.QWidget.__init__(self, parent)
        self.buttMinimumSize = QtCore.QSize(36,36)
        self.iconSize        = QtCore.QSize(28,28)
        icon1 = parent.icons['roiRectIcon']
        icon2 = parent.icons['roiPolyIcon']           
        self.button1 = QtGui.QPushButton(icon1,"")
        self.button2 = QtGui.QPushButton(icon2,"")
        self.button1.setIconSize(self.iconSize)
        self.button2.setIconSize(self.iconSize)
        self.button1.setMinimumSize(self.buttMinimumSize)
        self.button2.setMinimumSize(self.buttMinimumSize)
        self.button1.setToolTip('Add rectangular ROI')            
        self.button2.setToolTip('Add polyline ROI')       
        # Set the layout
        layout = QtGui.QHBoxLayout(self)            
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)                 
        self.setLayout(layout)
        self.adjustSize()
        widget.setContentsMargins(0,0,0,0)
        # Tag this widget as a popup
        self.setWindowFlags(QtCore.Qt.Popup)
        # Handle to widget (Pushbutton in sidepanel)
        self.widget = widget
        # Close popup if one of the buttons are pressed
        self.button1.clicked.connect(self.hide)
        self.button2.clicked.connect(self.hide)

    def update(self):       
        # Move to top right of pushbutton
        point = self.widget.rect().topRight()
        global_point = self.widget.mapToGlobal(point)
        self.move(global_point)      
            
    def leaveEvent(self,ev):
        self.hide()            