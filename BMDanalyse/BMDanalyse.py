# -*- coding: utf-8 -*-

# Copyright (C) 2013 Michael Hogg

# This file is part of BMDanalyse - See LICENSE.txt for information on usage and redistribution

import os, sys, matplotlib, matplotlib.pyplot
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
import numpy as np
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
import matplotlib_fix
import matplotlib.backends.qt4_editor.figureoptions as figureoptions
figureoptions.figure_edit = matplotlib_fix.figure_edit
from PIL import Image
import types

from customItems import QActionCustom
from ViewBoxCustom import MultiRoiViewBox, ImageAnalysisViewBox
from SidePanel import SidePanel
from version import __version__

absDirPath = os.path.dirname(__file__)  
    
class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
    
        QtGui.QMainWindow.__init__(self, parent) 
        self.loadIcons()   
        self.setupUserInterface() 
        self.setupSignals()    
        self.__version__ = __version__
        
        # Initialise variables
        self.imageFiles = {}
        self.timeData   = None
        self.plotWin    = None
        self.imageWin   = None
        self.BMDchange  = None
        self.roiNames   = None  
        
    def loadIcons(self):
        """ Load icons """
        self.icons = dict([
            ('BMDanalyseIcon', QtGui.QIcon(os.path.join(absDirPath,"icons","logo.png"))),
            ('imageAddIcon',   QtGui.QIcon(os.path.join(absDirPath,"icons","file_add.png"))),
            ('imageRemIcon',   QtGui.QIcon(os.path.join(absDirPath,"icons","file_delete2.png"))),
            ('imageDownIcon',  QtGui.QIcon(os.path.join(absDirPath,"icons","arrow-up-2.png"))),
            ('imageUpIcon',    QtGui.QIcon(os.path.join(absDirPath,"icons","arrow-down-2.png"))),
            ('imagePrevIcon',  QtGui.QIcon(os.path.join(absDirPath,"icons","arrow-left.png"))),
            ('imageNextIcon',  QtGui.QIcon(os.path.join(absDirPath,"icons","arrow-right.png"))),          
            ('roiAddIcon',     QtGui.QIcon(os.path.join(absDirPath,"icons","green-add3.png"))),
            ('roiRectIcon',    QtGui.QIcon(os.path.join(absDirPath,"icons","rectangularIcon.png"))),
            ('roiPolyIcon',    QtGui.QIcon(os.path.join(absDirPath,"icons","polygonIcon.png"))),
            ('roiRemIcon',     QtGui.QIcon(os.path.join(absDirPath,"icons","red_delete.png"))),
            ('roiSaveIcon',    QtGui.QIcon(os.path.join(absDirPath,"icons","filesave.png"))),
            ('roiCopyIcon',    QtGui.QIcon(os.path.join(absDirPath,"icons","file_copy.png"))),
            ('roiLoadIcon',    QtGui.QIcon(os.path.join(absDirPath,"icons","opened-folder.png")))])
        
    def setupUserInterface(self):
        """ Initialise the User Interface """

        # Left frame
        leftFrame = QtGui.QFrame()
        leftFrameLayout = QtGui.QHBoxLayout() 
        leftFrame.setLayout(leftFrameLayout)
        leftFrame.setLineWidth(0)
        leftFrame.setFrameStyle(QtGui.QFrame.Panel)
        leftFrameLayout.setContentsMargins(0,0,5,0)

        # Left frame contents     
        self.viewMain = GraphicsLayoutWidget()  # A GraphicsLayout within a GraphicsView 
        leftFrameLayout.addWidget(self.viewMain)
        self.viewMain.setMinimumSize(200,200)
        self.vb = MultiRoiViewBox(lockAspect=True,enableMenu=True)
        self.viewMain.addItem(self.vb)
        self.vb.disableAutoRange()
    
        # Right frame
        self.sidePanel = SidePanel(self) 
     
        # UI window (containing left and right frames)
        UIwindow         = QtGui.QWidget(self)
        UIwindowLayout   = QtGui.QHBoxLayout()
        UIwindowSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        UIwindowLayout.addWidget(UIwindowSplitter)
        UIwindow.setLayout(UIwindowLayout)
        self.setCentralWidget(UIwindow)
        UIwindowSplitter.addWidget(leftFrame)
        UIwindowSplitter.addWidget(self.sidePanel)  
 
        # Application window
        self.setWindowTitle('BMDanalyse')
        self.setWindowIcon(self.icons['BMDanalyseIcon'])
        self.setMinimumSize(600,500)
        self.resize(self.minimumSize())
       
        # Window menus       
        self.createMenus()     
        self.createActions() 

    def createMenus(self):
        
        # Menus 
        menubar          = self.menuBar()
        self.fileMenu    = menubar.addMenu('&File')
        self.roiMenu     = menubar.addMenu('&ROIs')
        self.submenu     = self.roiMenu.addMenu(self.icons['roiAddIcon'],"Add ROI")
        self.analyseMenu = menubar.addMenu('&Analyse')
        self.aboutMenu   = menubar.addMenu('A&bout')
        
    def createActions(self):    
   
        # Actions for File menu
        self.loadImageAct   = QtGui.QAction(self.icons['imageAddIcon'], "&Load image(s)",        self, shortcut="Ctrl+L")
        self.removeImageAct = QtGui.QAction(self.icons['imageRemIcon'], "&Remove current image", self, shortcut="Ctrl+X") 
        self.exitAct        = QtGui.QAction("&Quit", self, shortcut="Ctrl+Q",statusTip="Exit the application")
        fileMenuActions  = [self.loadImageAct,self.removeImageAct,self.exitAct]
        fileMenuActFuncs = [self.loadImages,self.removeImage,self.close]
        for i in xrange(len(fileMenuActions)):
            action   = fileMenuActions[i]
            function = fileMenuActFuncs[i]
            action.triggered[()].connect(function)
        self.fileMenu.addAction(self.loadImageAct)
        self.fileMenu.addAction(self.removeImageAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)        
       
        # Actions for ROI menu
        # Submenu to add ROIs
     
        #self.addROIRectAct = QActionCustom("Rectangular",self.submenu)
        #self.addROIPolyAct = QActionCustom("Polygon",self.submenu)
        self.addROIRectAct = QtGui.QAction("Rectangular",self.submenu)
        self.addROIPolyAct = QtGui.QAction("Polygon",self.submenu)
        
        #self.addROIRectAct.clickEvent.connect(self.vb.addROI)
        #self.addROIPolyAct.clickEvent.connect(self.vb.addPolyRoiRequest) 
        self.addROIRectAct.triggered[()].connect(self.vb.addROI)
        self.addROIPolyAct.triggered[()].connect(self.vb.addPolyRoiRequest) 
        
        self.submenu.addAction(self.addROIRectAct)
        self.submenu.addAction(self.addROIPolyAct)    

        self.addROIRectAct.setIcon(self.icons['roiRectIcon'])
        self.addROIPolyAct.setIcon(self.icons['roiPolyIcon'])
      
        self.addROIRectAct.setShortcut("Ctrl+Shift+R")
        self.addROIPolyAct.setShortcut("Ctrl+Shift+P")  
      
        self.loadRoiAct = QtGui.QAction(self.icons['roiLoadIcon'], "L&oad ROI",   self, shortcut="Ctrl+O")                          
        self.copyRoiAct = QtGui.QAction(self.icons['roiCopyIcon'], "&Copy ROI",   self, shortcut="Ctrl+C")     
        self.saveRoiAct = QtGui.QAction(self.icons['roiSaveIcon'], "&Save ROI",   self, shortcut="Ctrl+S") 
        self.remRoiAct  = QtGui.QAction(self.icons['roiRemIcon'] , "&Remove ROI", self, shortcut="Ctrl+D")
        roiMenuActions  = [self.loadRoiAct,self.copyRoiAct,self.saveRoiAct,self.remRoiAct]
        roiMenuActFuncs = [self.vb.loadROI,self.vb.copyROI,self.vb.saveROI,self.vb.removeROI]        
        for i in xrange(len(roiMenuActions)):
            action   = roiMenuActions[i]
            function = roiMenuActFuncs[i]
            action.triggered[()].connect(function)
            self.roiMenu.addAction(action)
             
        # Actions for Analyse menu
        self.roiAnalysisAct = QtGui.QAction("&ROI analysis", self.viewMain, shortcut="Ctrl+R",triggered=self.getBMD)
        self.imgAnalysisAct = QtGui.QAction("&Image analysis", self.viewMain, shortcut="Ctrl+I",triggered=self.imageAnalysis)
        self.analyseMenu.addAction(self.roiAnalysisAct) 
        self.analyseMenu.addAction(self.imgAnalysisAct)
       
        # Actions for 
        self.aboutAct = QtGui.QAction("&About", self.viewMain, shortcut='F1', triggered=self.onAbout)
        self.aboutMenu.addAction(self.aboutAct)
        
        
    def setupSignals(self):
        """ Setup signals """
        self.sidePanel.imageFileList.itemSelectionChanged.connect(self.getImageToDisplay)
        self.sidePanel.buttImageAdd.clicked.connect(self.loadImages)
        self.sidePanel.buttImageRem.clicked.connect(self.removeImage)
        self.sidePanel.buttImageUp.clicked.connect(self.sidePanel.moveImageUp)
        self.sidePanel.buttImageDown.clicked.connect(self.sidePanel.moveImageDown) 
        
        self.sidePanel.roiMenu.button1.clicked[()].connect(self.vb.addROI)
        self.sidePanel.roiMenu.button2.clicked[()].connect(self.vb.addPolyRoiRequest)           

        self.sidePanel.buttRoiCopy.clicked[()].connect(self.vb.copyROI)
        self.sidePanel.buttRoiRem.clicked.connect(self.vb.removeROI)        
        self.sidePanel.buttRoiLoad.clicked.connect(self.vb.loadROI)
        self.sidePanel.buttRoiSave.clicked.connect(self.vb.saveROI)
        #self.vb.sigROIchanged.connect(self.updateROItools)
        
    def onAbout(self):
        """ About BMDanalyse message"""
        author  ='Michael Hogg'
        date    ='2012 - 2013'        
        version = self.__version__
            
        QtGui.QMessageBox.about(self, 'About BMDanalyse', 
            """
            <b>BMDanalyse</b>
            <p>A simple program for the analysis of a time series of Bone Mineral Density (BMD) images.</p>
            <p>Used to evaluate the bone gain / loss in a number of regions of interest (ROIs) over time, 
            typically due to bone remodelling as a result of stress shielding around an orthopaedic implant.</p>
            <p><table border="0" width="150">
            <tr>
            <td>Author:</td>
            <td>%s</td>
            </tr>
            <tr>
            <td>Version:</td>
            <td>%s</td>
            </tr>
            <tr>
            <td>Date:</td>
            <td>%s</td>
            </tr>            
            </table></p>
            """ % (author,version,date))

    def updateROItools(self,roi=None):
        """ Update ROI info box in side panel """ 
        if roi==None:
            self.sidePanel.updateRoiInfoBox()
        else:           
            roiState    = roi.getState()
            posx,posy   = roiState['pos']
            sizex,sizey = roiState['size']
            angle       = roiState['angle']
            name  = roi.name
            pos   = '(%.3f, %.3f)' % (posx,posy)
            size  = '(%.3f, %.3f)' % (sizex,sizey)
            angle = '%.3f' % angle
            self.sidePanel.updateRoiInfoBox(name,pos,size,angle)  
    
    def loadImages(self):
        """ Load an image to be analysed """
        newImages = {}
        fileNames = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Load images"),QtCore.QDir.currentPath())
        
        # Fix for PySide. PySide doesn't support QStringList types. PyQt4 getOpenFileNames returns a QStringList, whereas PySide
        # returns a type (the first entry being the list of filenames).
        if isinstance(fileNames,types.TupleType): fileNames = fileNames[0]
        if hasattr(QtCore,'QStringList') and isinstance(fileNames, QtCore.QStringList): fileNames = [str(i) for i in fileNames]
        
        if len(fileNames)>0:
            for fileName in fileNames:
                if fileName!='':
                    imgarr = np.array(Image.open(str(fileName)))
                    imgarr = imgarr.swapaxes(0,1)
                    if   imgarr.ndim==2: imgarr = imgarr[:,::-1]
                    elif imgarr.ndim==3: imgarr = imgarr[:,::-1,:]                   
                    newImages[fileName] = imgarr
            
            # Add filenames to list widget. Only add new filenames. If filename exists aready, then
            # it will not be added, but data will be updated
            for fileName in sorted(newImages.keys()):
                if not self.imageFiles.has_key(fileName):
                    self.sidePanel.addImageToList(fileName)
                self.imageFiles[fileName] = newImages[fileName]
            
            # Show image in Main window
            self.vb.enableAutoRange()
            if self.sidePanel.imageFileList.currentRow()==-1: self.sidePanel.imageFileList.setCurrentRow(0)
            self.showImage(str(self.sidePanel.imageFileList.currentItem().text()))
            self.vb.disableAutoRange()            
            
    def removeImage(self):
        """ Remove image from sidePanel imageFileList """
        
        # Return if there is no image to remove
        if self.vb.img==None: return
        
        # Get current image in sidePanel imageFileList and remove from list
        currentRow = self.sidePanel.imageFileList.currentRow()
        image      = self.sidePanel.imageFileList.takeItem(currentRow)
        imageName  = str(image.text())
        
        # Delete key and value from dictionary 
        if imageName!='': del self.imageFiles[imageName]
        #self.imageFiles.pop(imageName,None)
        
        # Get image item in imageFileList to replace deleted image
        if self.sidePanel.imageFileList.count()==0:
            self.vb.enableAutoRange()
            self.vb.removeItem(self.vb.img)
            self.vb.showImage(None)
            #self.vb.img = None
            self.vb.disableAutoRange()
        else: 
            currentRow = self.sidePanel.imageFileList.currentRow()
            imageName  = str(self.sidePanel.imageFileList.item(currentRow).text())
            self.showImage(imageName)   

    def showImage(self,imageFilename):
        """ Shows image in main view """
        self.arr = self.imageFiles[imageFilename]
        self.vb.showImage(self.arr)
    
    def getImageToDisplay(self):
        """ Get current item in file list and display in main view"""
        try:    imageFilename = str(self.sidePanel.imageFileList.currentItem().text())
        except: pass
        else:   self.showImage(imageFilename)  

    def getBMD(self):
        """ Get change in BMD over time (e.g. for each image) for all ROIs. 
            
            Revised function that converts the list of images into a 3D array
            and then uses the relative position of the ROIs to the current
            image, self.vb.img, to get the average BMD value e.g. it doesn't use
            setImage to change the image in the view. This requires that all
            images are the same size and in the same position.
        """
        
        # Return if there is no image or rois in view
        if self.vb.img==None or len(self.vb.rois)==0: return               
        
        # Collect all images into a 3D array
        imageFilenames = self.sidePanel.getListOfImages()
        images    = [self.imageFiles[str(name.text())] for name in imageFilenames]
        imageData = np.dstack(images)
        numImages = len(images)           
        
        # Get BMD across image stack for each ROI
        numROIs = len(self.vb.rois)
        BMD     = np.zeros((numImages,numROIs),dtype=float) 
        self.roiNames = []   
        for i in xrange(numROIs):
            roi = self.vb.rois[i]
            self.roiNames.append(roi.name)
            arrRegion   = roi.getArrayRegion(imageData,self.vb.img, axes=(0,1))
            avgROIvalue = arrRegion.mean(axis=0).mean(axis=0)
            BMD[:,i]    = avgROIvalue
        
        # Calculate the BMD change (percentage of original)
        tol = 1.0e-06
        for i in xrange(numROIs):
            if abs(BMD[0,i])<tol: 
                BMD[:,i] = 100.
            else: 
                BMD[:,i] = BMD[:,i] / BMD[0,i] * 100.
        self.BMDchange = BMD-100.
        if self.timeData==None or self.timeData.size!=numImages:
            self.timeData = np.arange(numImages,dtype=float)
        
        # Plot results  
        self.showResults()
        
    def imageAnalysis(self):
        # Generate images of BMD change
        if self.vb.img==None: return
        self.showImageWin()
        
    def sliderValueChanged(self,value):
        self.imageWin.sliderLabel.setText('BMD change: >= %d %s' % (value,'%'))
        self.setLookupTable(value)
        self.imageWin.vb.img2.setLookupTable(self.lut)
        
    def setLookupTable(self,val):
        lut = []
        for i in range(256):
            if   i > 127+val:
                lut.append(matplotlib.cm.jet(255))
            elif i < 127-val:    
                lut.append(matplotlib.cm.jet(0))
            else:
                lut.append((0.0,0.0,0.0,0.0)) 
        lut = np.array(lut)*255
        self.lut = np.array(lut,dtype=np.ubyte)
     
    def createImageWin(self):
    
        self.buttMinimumSize = QtCore.QSize(70,36)
        self.iconSize = QtCore.QSize(24,24)
        
        if self.imageWin==None:
            
            self.imageWin = QtGui.QDialog(self, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint |  \
                                          QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
            self.imageWin.setWindowTitle('BMDanalyse')
            self.imageWin.setWindowIcon(self.icons['BMDanalyseIcon'])
            self.imageWin.setMinimumSize(250,500)
            self.imageWin.resize(self.imageWin.minimumSize()) 
            
            # Create viewBox  
            self.imageWin.glw = GraphicsLayoutWidget()  # A GraphicsLayout within a GraphicsView 
            self.imageWin.vb  = ImageAnalysisViewBox(lockAspect=True,enableMenu=True)
            self.imageWin.vb.disableAutoRange()
            self.imageWin.glw.addItem(self.imageWin.vb) 
            arr = self.imageFiles.values()[0]
            self.imageWin.vb.img1 = pg.ImageItem(arr,autoRange=False,autoLevels=False)
            self.imageWin.vb.addItem(self.imageWin.vb.img1)      
            self.imageWin.vb.img2 = pg.ImageItem(None,autoRange=False,autoLevels=False)
            self.imageWin.vb.addItem(self.imageWin.vb.img2)
            self.imageWin.vb.autoRange()
            lut = [ [ int(255*val) for val in matplotlib.cm.gray(i)[:3] ] for i in xrange(256) ]
            lut = np.array(lut,dtype=np.ubyte)         
            self.imageWin.vb.img1.setLookupTable(lut)
            
            # Label to show index of current image label
            self.imageCurrCont = QtGui.QFrame()
            self.imageCurrCont.setLineWidth(2)
            self.imageCurrCont.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
            self.imageCurrCont.setMinimumWidth(70)
            self.imageWin.currLabel = QtGui.QLabel("")
            self.imageWin.currLabel.setAlignment(QtCore.Qt.AlignHCenter)            
            imageCurrContLayout = QtGui.QHBoxLayout()
            imageCurrContLayout.addWidget(self.imageWin.currLabel)
            self.imageCurrCont.setLayout(imageCurrContLayout)  
            
            # Create buttons to select images
            self.imageWin.buttCont = QtGui.QWidget()
            self.imageWin.buttPrev = QtGui.QPushButton(self.icons['imagePrevIcon'],"")
            self.imageWin.buttNext = QtGui.QPushButton(self.icons['imageNextIcon'],"")
            self.buttLayout = QtGui.QHBoxLayout()
            self.buttLayout.addStretch(1)
            self.buttLayout.addWidget(self.imageWin.buttPrev)
            self.buttLayout.addWidget(self.imageCurrCont)
            self.buttLayout.addWidget(self.imageWin.buttNext)
            self.buttLayout.addStretch(1)
            self.imageWin.buttCont.setLayout(self.buttLayout)
            self.imageWin.buttPrev.setMinimumSize(self.buttMinimumSize)
            self.imageWin.buttNext.setMinimumSize(self.buttMinimumSize)
            self.imageWin.buttPrev.setIconSize(self.iconSize) 
            self.imageWin.buttNext.setIconSize(self.iconSize)
            self.buttLayout.setContentsMargins(0,5,0,5)
            
            self.imageWin.buttPrev.clicked.connect(self.prevImage)
            self.imageWin.buttNext.clicked.connect(self.nextImage)
            
            # Create slider    
            self.imageWin.sliderCon = QtGui.QWidget()
            self.imageWin.slider = QtGui.QSlider(self)
            self.imageWin.slider.setOrientation(QtCore.Qt.Horizontal)
            self.imageWin.slider.setMinimum(1)
            self.imageWin.slider.setMaximum(100)
            self.imageWin.slider.setMinimumWidth(100)
            self.imageWin.slider.valueChanged.connect(self.sliderValueChanged)
            self.imageWin.sliderLabel = QtGui.QLabel('1')
            self.imageWin.sliderLabel.setMinimumWidth(120)
            self.sliderLayout = QtGui.QHBoxLayout()
            self.sliderLayout.addStretch(1)
            self.sliderLayout.addWidget(self.imageWin.sliderLabel)
            self.sliderLayout.addWidget(self.imageWin.slider)
            self.sliderLayout.addStretch(1)
            self.imageWin.sliderCon.setLayout(self.sliderLayout)
            self.sliderLayout.setContentsMargins(0,0,0,5)
            
            # Format image window
            self.imageWinLayout = QtGui.QVBoxLayout()
            self.imageWinLayout.addWidget(self.imageWin.glw)
            self.imageWinLayout.addWidget(self.imageWin.buttCont)
            self.imageWinLayout.addWidget(self.imageWin.sliderCon)
            self.imageWin.setLayout(self.imageWinLayout)
            
            self.imageWin.imagesRGB = None
            
        # Show
        self.imageWin.show()
        self.imageWin.slider.setValue(10)
        self.sliderValueChanged(10)
        self.imageWinIndex = 0
        
    def prevImage(self):
        #numImages = len(self.imageFiles)
        minIndex  = 0
        currIndex = self.imageWinIndex 
        prevIndex = currIndex - 1 
        self.imageWinIndex = max(prevIndex,minIndex)    
        self.updateImageWin()
        
    def nextImage(self):
        numImages = len(self.imageFiles)
        maxIndex  = numImages - 1
        currIndex = self.imageWinIndex
        nextIndex = currIndex + 1 
        self.imageWinIndex = min(nextIndex,maxIndex)
        self.updateImageWin()
        
    def updateImageWin(self):
        imageFilenames = self.sidePanel.getListOfImages()
        imageName      = imageFilenames[self.imageWinIndex]
        self.imageWin.vb.img1.setImage(self.imageFiles[str(imageName.text())],autoLevels=False) 
        self.imageWin.vb.img2.setImage(self.imageWin.imagesRGB[self.imageWinIndex],autoLevels=False) 
        self.imageWin.currLabel.setText("%i / %i" % (self.imageWinIndex+1,len(imageFilenames)))
        
    def showImageWin(self):
        self.createImageWin()
        #if self.imageWin.imagesRGB == None: self.imagesBMDpercentChange()
        self.imagesBMDpercentChange()
        self.updateImageWin()

    def imagesBMDpercentChange(self):
        
        # Get image arrays and convert to an array of floats
        imageFilenames = self.sidePanel.getListOfImages()
        images         = [ self.imageFiles[str(name.text())] for name in imageFilenames ]
        imagesConv = []
        for img in images: 
            image = img.copy()
            image[np.where(image==0)] = 1
            image = image.astype(np.float)
            imagesConv.append(image)
               
        # Calculate percentage change and set with limits -100% to +100%
        imagesPercCh = []
        imageInitial = imagesConv[0]
        for image in imagesConv:
            imagePercCh = (image-imageInitial)/imageInitial*100.
            imagePercCh[np.where(imagePercCh> 100.)] =  100.
            imagePercCh[np.where(imagePercCh<-100.)] = -100.
            imagesPercCh.append(imagePercCh)
            
        numImages  = len(imagesPercCh)
        self.imageWin.imagesRGB = []    
        for i in xrange(numImages):
            image = imagesPercCh[i]
            sx,sy = image.shape 
            #imageCh  = np.zeros((sx,sy),dtype=np.float)
            imageRGB = image*(255/200.)+(255/2.)
            self.imageWin.imagesRGB.append(imageRGB)
        
    def BMDtoCSVfile(self):
        """ Write BMD change to csv file """
        fileName = QtGui.QFileDialog.getSaveFileName(None,self.tr("Export to CSV"),QtCore.QDir.currentPath(),self.tr("CSV (*.csv)"))
        # Fix for PyQt/PySide compatibility. PyQt returns a QString, whereas PySide returns a tuple (first entry is filename as string)        
        if isinstance(fileName,types.TupleType): fileName = fileName[0]
        if hasattr(QtCore,'QString') and isinstance(fileName, QtCore.QString): fileName = str(fileName)            
        if not fileName=='':        
        #if not fileName.isEmpty():               
            textFile  = open(fileName,'w')
            numFrames, numROIs = self.BMDchange.shape    
            roiNames = self.roiNames
            header  = "%10s," % 'Time'
            header += ((numROIs-1)*'%10s,'+'%10s\n') % tuple(roiNames)
            textFile.write(header)
            for i in xrange(numFrames):
                textFile.write('%10.1f,' % self.timeData[i])
                for j in xrange(numROIs):
                    if j<numROIs-1: fmt = '%10.3f,'
                    else:           fmt = '%10.3f\n'
                    textFile.write(fmt % self.BMDchange[i,j])
            textFile.close()       

    def showResults(self,):
        """ Plots BMD change using matplotlib """
        # Create plot window       
        if self.plotWin==None:
            self.plotWin = QtGui.QDialog(self, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint |  \
                                         QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
            self.plotWin.setWindowTitle('BMDanalyse')
            self.plotWin.setWindowIcon(self.icons['BMDanalyseIcon'])
            self.plotWin.setMinimumSize(600,500)
            self.plotWin.resize(self.minimumSize()) 

            # Create Matplotlib widget
            self.mplw = MatplotlibWidget(size=(5,6))
            self.fig  = self.mplw.getFigure()
        
            self.editDataButton  = QtGui.QPushButton('Edit plot')
            self.exportCSVButton = QtGui.QPushButton('Export data')
            self.mplw.toolbar.addWidget(self.editDataButton)
            self.mplw.toolbar.addWidget(self.exportCSVButton)
            self.editDataButton.clicked.connect(self.showEditBox)
            self.exportCSVButton.clicked.connect(self.BMDtoCSVfile)

            # Format plot window
            self.plotWinLayout = QtGui.QVBoxLayout()
            self.plotWinLayout.addWidget(self.mplw)
            self.plotWin.setLayout(self.plotWinLayout)
        
        self.createFigure()
        self.plotWin.show()
        self.mplw.draw()
        
    def createFigure(self):
        """ Creates plot of results """
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.clear()
        self.fig.subplots_adjust(bottom=0.15,top=0.85,left=0.15,right=0.925)
        numFrames, numROIs = self.BMDchange.shape
        t = self.timeData
        # Plot data
        for i in xrange(numROIs):
            roiname = self.roiNames[i]
            self.ax1.plot(t,self.BMDchange[:,i],'-o',label=roiname,linewidth=2.0)
        kwargs = dict(y=1.05)  # Or kwargs = {'y':1.05}
        self.ax1.set_title('Change in Bone Mineral Density over time',fontsize=14,fontweight='roman',**kwargs)
        self.ax1.set_xlabel('Time',fontsize=10)
        self.ax1.set_ylabel('Change in BMD (%)',fontsize=10)
        self.ax1.legend(loc=0)
        matplotlib.pyplot.setp(self.ax1.get_xmajorticklabels(),  fontsize=10)
        matplotlib.pyplot.setp(self.ax1.get_ymajorticklabels(),  fontsize=10)
        matplotlib.pyplot.setp(self.ax1.get_legend().get_texts(),fontsize=10)  
        self.ax1.grid()  

    def fillEditBox(self):
        rows,cols = self.BMDchange.shape
        for i in xrange(rows):
            itmValue = '%.2f' % self.timeData[i]
            itm      = QtGui.QTableWidgetItem(itmValue)
            self.tableResults.setItem(i,0,itm)
            for j in xrange(cols):
                itmValue = '%.2f' % self.BMDchange[i,j]
                itm = QtGui.QTableWidgetItem(itmValue)
                self.tableResults.setItem(i,j+1,itm)

    def showEditBox(self):
        self.plotWin.editBox = QtGui.QDialog(self.plotWin, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.plotWin.editBox.setWindowIcon(self.icons['BMDanalyseIcon']) 
        self.plotWin.editBox.setWindowTitle('BMDanalyse') 
        self.plotWin.editBox.setModal(True)
        # Add table
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(10,10,10,10)
        layout.setSpacing(20)
        rows,cols = self.BMDchange.shape
        self.tableResults = MyTableWidget(rows,cols+1,self.plotWin.editBox)
        self.tableResults.verticalHeader().setVisible(True)
        # Set headers
        self.tableResults.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem('Time'))
        for i in xrange(cols):
            header = QtGui.QTableWidgetItem(self.roiNames[i])
            self.tableResults.setHorizontalHeaderItem(i+1,header)
        # Add values to table
        self.fillEditBox()
        # Set layout
        layout.addWidget(self.tableResults)
        self.buttonsFrame  = QtGui.QFrame()
        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonReset   = QtGui.QPushButton('Reset')
        self.buttonSave    = QtGui.QPushButton('Save')
        self.buttonClose   = QtGui.QPushButton('Cancel')
        self.buttonReset.setFixedWidth(50)
        self.buttonSave.setFixedWidth(50)
        self.buttonClose.setFixedWidth(50)
        self.buttonClose.clicked.connect(self.plotWin.editBox.close)
        self.buttonSave.clicked.connect(self.updateTableValues)
        self.buttonReset.clicked.connect(self.fillEditBox)
        self.buttonsLayout.addStretch(1)
        self.buttonsLayout.addWidget(self.buttonReset)
        self.buttonsLayout.addWidget(self.buttonSave)
        self.buttonsLayout.addWidget(self.buttonClose) 
        self.buttonsLayout.setContentsMargins(0,0,0,0) 
        self.buttonsFrame.setLayout(self.buttonsLayout)
        layout.addWidget(self.buttonsFrame)
        self.plotWin.editBox.setLayout(layout)
        self.plotWin.editBox.setMaximumSize(layout.sizeHint())
        self.plotWin.editBox.show()
        
    def updateTableValues(self):        
        # Create temporary arrays
        timeData  = self.timeData.copy()
        BMDchange = self.BMDchange.copy() 
        # Put the values from the tables into the temporary arrays
        rows = self.tableResults.rowCount()
        cols = self.tableResults.columnCount()
        for r in xrange(rows):
            for c in xrange(cols):
                item      = self.tableResults.item(r,c)
                itemValue = float(item.text())
                if c==0:
                    timeData[r] = itemValue 
                else: 
                    BMDchange[r,c-1] = itemValue
        # Check that time values are in increasing order. If so, then update arrays
        if any(np.diff(timeData)<=0):
            self.errorMessage = QtGui.QMessageBox()
            self.errorMessage.setWindowIcon(self.icons['BMDanalyseIcon'])
            self.errorMessage.setWindowTitle('BMDanalyse')
            self.errorMessage.setText('Input error: Time values should be in order of increasing value')
            self.errorMessage.setIcon(QtGui.QMessageBox.Warning)           
            self.errorMessage.open()         
        else:         
            self.timeData  = timeData
            self.BMDchange = BMDchange
            self.createFigure()
            self.mplw.draw()
            self.plotWin.editBox.close()


class MyTableWidget(QtGui.QTableWidget):  
    def __init__(self, x, y, parent = None):
        super(MyTableWidget, self).__init__(x, y, parent)

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

        
def run():
    # PySide fix: Check if QApplication already exists. Create QApplication if it doesn't exist 
    app=QtGui.QApplication.instance()        
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
