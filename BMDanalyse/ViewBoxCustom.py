# -*- coding: utf-8 -*-

# Copyright (C) 2016 Michael Hogg

# This file is part of BMDanalyse - See LICENSE.txt for information on usage and redistribution

import pyqtgraph as pg
import numpy as np
import matplotlib
import pickle
import pyqtgraph.functions as fn
import types
from pyqtgraph.Qt import QtCore, QtGui
from ROI import RectROIcustom, PolyLineROIcustom
from customItems import QMenuCustom, ImageExporterCustom
from functools import partial

__all__=['ImageAnalysisViewBox','ViewMode','MultiRoiViewBox']

class ImageAnalysisViewBox(pg.ViewBox):

    '''
    Custom ViewBox used to over-ride the context menu. I don't want the full context menu, 
    just a view all and an export. Export does not call a dialog, just prompts user for filename.
    '''

    def __init__(self,parent=None,border=None,lockAspect=False,enableMouse=True,invertY=False,enableMenu=True,name=None):
        pg.ViewBox.__init__(self,parent,border,lockAspect,enableMouse,invertY,enableMenu,name)
   
        self.menu = None # Override pyqtgraph ViewBoxMenu 
        self.menu = self.getMenu(None)       
        
    def raiseContextMenu(self, ev):
        if not self.menuEnabled(): return
        menu = self.getMenu(ev)
        pos  = ev.screenPos()
        menu.popup(QtCore.QPoint(pos.x(), pos.y()))
        
    def export(self):
        self.exp = ImageExporterCustom(self)
        self.exp.export()

    def getMenu(self,event):
        if self.menu is None:
            self.menu        = QMenuCustom()
            self.viewAll     = QtGui.QAction("View All", self.menu)
            self.exportImage = QtGui.QAction("Export image", self.menu)
            self.viewAll.triggered[()].connect(self.autoRange)
            self.exportImage.triggered[()].connect(self.export)
            self.menu.addAction(self.viewAll)
            self.menu.addAction(self.exportImage)
        return self.menu 
 
 
class ViewMode():
    ''' Helper class for different colour displays of images in MultiRoiViewBox class '''
    def __init__(self,id,cmap):
        self.id   = id
        self.cmap = cmap
        self.getLookupTable()
    def getLookupTable(self):        
        lut = [ [ int(255*val) for val in self.cmap(i)[:3] ] for i in xrange(256) ]
        lut = np.array(lut,dtype=np.ubyte)
        self.lut = lut     


class MultiRoiViewBox(pg.ViewBox):
    
    ''' Custom Viewbox for multiple ROIs '''

    def __init__(self,parent=None,border=None,lockAspect=False,enableMouse=True,invertY=False,enableMenu=True,name=None):
        pg.ViewBox.__init__(self,parent,border,lockAspect,enableMouse,invertY,enableMenu,name)
        # Set default values
        self.rois = []
        self.currentROIindex = None
        self.img         = None    
        self.NORMAL      = ViewMode(0,matplotlib.cm.gray)  
        self.DEXA        = ViewMode(1,matplotlib.cm.jet)
        self.viewMode    = self.NORMAL
        self.drawROImode = False
        self.drawingROI  = None
        self.menu        = None
        
    def getContextMenus(self,ev):
        return None
        
    def raiseContextMenu(self, ev):
        ''' Display context menu at location of right mouse click '''
        if not self.menuEnabled(): return
        menu = self.getMenu(ev)
        pos  = ev.screenPos()
        menu.popup(QtCore.QPoint(pos.x(), pos.y()))
        
    def export(self):
        ''' Export viewbox image '''
        self.exp = ImageExporterCustom(self)
        self.exp.export()
        
    def raiseRoiSelectMenuLeft(self,ev,roiList):
        ''' Raise roi menu on left mouse click '''        
        self.roimenu = QtGui.QMenu()
        for roi in roiList:
            action = QtGui.QAction(roi.name, self.roimenu)
            action.triggered[()].connect(lambda arg=roi: self.selectROI(arg))     
            self.roimenu.addAction(action)
        pos = ev.screenPos()
        self.roimenu.popup(QtCore.QPoint(pos.x(), pos.y()))
        
    def raiseRoiSelectMenuRight(self,ev,roiList):
        ''' Raise roi menu on right mouse click 
            Must use functools.partial (not lamda) here to get signals to work here '''
        self.roimenu = QtGui.QMenu()
        for roi in roiList:
            action = QtGui.QAction(roi.name, self.roimenu)
            action.triggered[()].connect(partial(roi.raiseContextMenu, ev))
            self.roimenu.addAction(action)
        pos = ev.screenPos()
        self.roimenu.popup(QtCore.QPoint(pos.x(), pos.y()))
            
    def mouseClickEvent(self, ev):
        ''' Mouse click event handler '''        
        # Check if click is over any rois
        roisUnderMouse = []
        pos = ev.scenePos()
        for roi in self.rois:
            if roi.isUnderMouse(pos):
                roisUnderMouse.append(roi)
        numRois = len(roisUnderMouse)
        # Drawing mode (all buttons)        
        if self.drawROImode:
            ev.accept()
            self.drawPolygonRoi(ev)
        # Click not over any rois
        elif numRois==0:
            # Context menu (right mouse button)
            if ev.button() == QtCore.Qt.RightButton and self.menuEnabled():
                self.raiseContextMenu(ev)         
        # Click over any rois      
        else:
            if ev.button() == QtCore.Qt.LeftButton:       
                if numRois==1:
                    self.selectROI(roisUnderMouse[0])
                elif numRois>1:
                    self.raiseRoiSelectMenuLeft(ev,roisUnderMouse)
            elif ev.button() == QtCore.Qt.RightButton: 
                if numRois==1:
                    roisUnderMouse[0].raiseContextMenu(ev)
                elif numRois>1:
                    self.raiseRoiSelectMenuRight(ev,roisUnderMouse)            
           
    def addPolyRoiRequest(self):
        ''' Function to add a Polygon ROI '''
        self.drawROImode = True

    def endPolyRoiRequest(self):
        ''' Called at the completion of drawing Polygon ROI '''
        self.drawROImode = False  # Deactivate drawing mode
        self.drawingROI  = None   # No roi being drawn, so set to None
         
    def addPolyLineROI(self,handlePositions):
        ''' Add Polygon ROI - Used for copy and load operations '''
        roi = PolyLineROIcustom(handlePositions=handlePositions,removable=True)
        roi.setName('ROI-%i'% self.getROIid())
        self.addItem(roi)                      # Add roi to viewbox
        self.rois.append(roi)                  # Add to list of rois
        self.selectROI(roi)
        self.sortROIs()  
        self.setCurrentROIindex(roi)  
        roi.translatable = True
        for seg in roi.segments:
            seg.setSelectable(True)
        for h in roi.handles:
            h['item'].setSelectable(True)
        # Setup signals
        roi.sigRemoveRequested.connect(self.removeROI)
        roi.sigCopyRequested.connect(self.copyROI)
        roi.sigSaveRequested.connect(self.saveROI)            

    def drawPolygonRoi(self,ev):
        ''' Function to draw a Polygon ROI - Called directly by MouseClickEvent '''
        roi = self.drawingROI
        pos = self.mapSceneToView(ev.scenePos())
        # TO DRAW ROI
        if ev.button() == QtCore.Qt.LeftButton:
            if roi is None:                                  # To start drawing a new roi
                roi = PolyLineROIcustom(removable = False)   # Create new roi
                roi.setName('ROI-%i'% self.getROIid())       # Set name. Do this before self.selectROIs(roi)
                self.drawingROI = roi                      
                self.addItem(roi)                            # Add roi to viewbox
                self.rois.append(roi)                        # Add to list of rois
                self.selectROI(roi)                          # Make selected
                self.sortROIs()                              # Sort list of rois
                self.setCurrentROIindex(roi)                 # Make current 
                roi.translatable = False                     # Deactivate translation during drawing
                roi.addFreeHandle(pos)                       # Add two handles on first click (1 fixed, 1 draggable)
                roi.addFreeHandle(pos)
                h = roi.handles[-1]['item']                  # Get draggable handle
                h.scene().sigMouseMoved.connect(h.movePoint) # Connect signal to move handle with mouse
            else:                                            # To continue drawing an existing roi
                h = roi.handles[-1]['item']                  # Get last handle
                h.scene().sigMouseMoved.disconnect()         # Make last handle non-draggable  
                roi.addFreeHandle(pos)                       # Add new handle
                h = roi.handles[-1]['item']                  # Get new handle
                h.scene().sigMouseMoved.connect(h.movePoint) # Make new handle draggable  
            # Add a segment between the handles
            roi.addSegment(roi.handles[-2]['item'],roi.handles[-1]['item'])
            # Set segment and handles to non-selectable
            seg = roi.segments[-1]
            seg.setSelectable(False)
            for h in seg.handles:
                h['item'].setSelectable(False)
        # TO STOP DRAWING ROI
        elif (ev.button() == QtCore.Qt.MiddleButton) or \
             (ev.button() == QtCore.Qt.RightButton and (roi==None or len(roi.segments)<3)):
            if roi!=None:
                # Remove handle and disconnect from scene
                h = roi.handles[-1]['item']
                h.scene().sigMouseMoved.disconnect()
                roi.removeHandle(h)
                # Removed roi from viewbox
                self.removeItem(roi)
                self.rois.pop(self.currentROIindex)
                self.setCurrentROIindex(None)
            # Exit ROI drawing mode
            self.endPolyRoiRequest()
        # TO COMPLETE ROI
        elif ev.button() == QtCore.Qt.RightButton:
            # Remove last handle
            h = roi.handles[-1]['item']
            h.scene().sigMouseMoved.disconnect()  
            roi.removeHandle(h)
            # Add segment to close ROI
            roi.addSegment(roi.handles[-1]['item'],roi.handles[0]['item'])
            # Setup signals on completed roi
            roi.sigRemoveRequested.connect(self.removeROI)
            roi.sigCopyRequested.connect(self.copyROI)
            roi.sigSaveRequested.connect(self.saveROI)
            # Re-activate mouse clicks for all roi, segments and handles
            roi.removable    = True
            roi.translatable = True  
            for seg in roi.segments:
                seg.setSelectable(True)
            for h in roi.handles:
                h['item'].setSelectable(True)
            # Exit ROI drawing mode
            self.endPolyRoiRequest()    

    def getMenu(self,ev):
        '''Create and return context menu '''
        # Menu and submenus
        self.menu          = QtGui.QMenu()
        self.submenu       = QtGui.QMenu("Add ROI", self.menu)           
        # Actions
        self.addROIRectAct = QtGui.QAction("Rectangular", self.submenu)
        self.addROIPolyAct = QtGui.QAction("Polygon", self.submenu)
        self.loadROIAct    = QtGui.QAction("Load ROI", self.menu)
        self.dexaMode      = QtGui.QAction("Toggle normal/DEXA view", self.menu)
        self.viewAll       = QtGui.QAction("View All", self.menu)
        self.exportImage   = QtGui.QAction("Export image", self.menu)
        # Signals
        self.loadROIAct.triggered[()].connect(self.loadROI)
        self.dexaMode.triggered.connect(self.toggleViewMode)
        self.viewAll.triggered[()].connect(self.autoRange)
        self.exportImage.triggered[()].connect(self.export)
        self.addROIRectAct.triggered[()].connect(lambda arg=ev: self.addRoiRequest(arg))
        self.addROIPolyAct.triggered.connect(self.addPolyRoiRequest)
        # Add actions to menu and submenus
        self.submenu.addAction(self.addROIRectAct)
        self.submenu.addAction(self.addROIPolyAct)
        self.menu.addAction(self.viewAll)
        self.menu.addAction(self.dexaMode)
        self.menu.addAction(self.exportImage)
        self.menu.addSeparator()
        self.menu.addMenu(self.submenu)
        self.menu.addAction(self.loadROIAct)
        self.dexaMode.setCheckable(True)
        # Return menu
        return self.menu
        
    def setCurrentROIindex(self,roi=None):
        ''' Use this function to change currentROIindex value to ensure a signal is emitted '''
        if roi==None: self.currentROIindex = None
        else:         self.currentROIindex = self.rois.index(roi)

    def getCurrentROIindex(self):
        return self.currentROIindex    
    
    def selectROI(self,roi):
        '''Selection control of ROIs'''
        # If no ROI is currently selected (currentROIindex is None), select roi
        if self.currentROIindex==None:
            roi.setSelected(True)
            self.setCurrentROIindex(roi)
        # If an ROI is already selected...
        else:
            roiSelected = self.rois[self.currentROIindex]
            roiSelected.setSelected(False) 
            # If a different roi is already selected, then select roi 
            if self.currentROIindex != self.rois.index(roi):
                self.setCurrentROIindex(roi)
                roi.setSelected(True)
            # If roi is already selected, then unselect
            else: 
                self.setCurrentROIindex(None)
    
    def addRoiRequest(self,ev):
        ''' Function to addROI at an event screen position '''
        # Get position
        pos  = self.mapSceneToView(ev.scenePos())
        xpos = pos.x()
        ypos = pos.y()
        # Shift down by size
        xr,yr = self.viewRange()
        xsize  = 0.25*(xr[1]-xr[0])
        ysize  = 0.25*(yr[1]-yr[0])
        xysize = min(xsize,ysize)
        if xysize==0: xysize=100       
        ypos -= xysize
        # Create ROI
        xypos = (xpos,ypos)
        self.addROI(pos=xypos)
        
    def addROI(self,pos=None,size=None,angle=0.0):
        ''' Add an ROI to the ViewBox '''    
        xr,yr = self.viewRange()
        if pos is None:
            posx = xr[0]+0.05*(xr[1]-xr[0])
            posy = yr[0]+0.05*(yr[1]-yr[0])
            pos  = [posx,posy]
        if size is None:
            xsize  = 0.25*(xr[1]-xr[0])
            ysize  = 0.25*(yr[1]-yr[0])
            xysize = min(xsize,ysize)
            if xysize==0: xysize=100
            size = [xysize,xysize]  
        roi = RectROIcustom(pos,size,angle,removable=True,pen=(255,0,0))
        # Setup signals
        roi.setName('ROI-%i'% self.getROIid()) 
        roi.sigRemoveRequested.connect(self.removeROI)
        roi.sigCopyRequested.connect(self.copyROI)
        roi.sigSaveRequested.connect(self.saveROI)
        # Keep track of rois
        self.addItem(roi)
        self.rois.append(roi)
        self.selectROI(roi)
        self.sortROIs()  
        self.setCurrentROIindex(roi)

    def sortROIs(self):
        ''' Sort self.rois by roi name and adjust self.currentROIindex as necessary '''
        if len(self.rois)==0: return 
        if self.currentROIindex==None:
            self.rois.sort()  
        else:
            roiCurrent = self.rois[self.currentROIindex]
            self.rois.sort()  
            self.currentROIindex = self.rois.index(roiCurrent)
    
    def getROIid(self):
        ''' Get available and unique number for ROI name '''
        nums = [ int(roi.name.split('-')[-1]) for roi in self.rois if roi.name!=None ]
        nid  = 1
        if len(nums)>0: 
            while(True):
                if nid not in nums: break
                nid+=1
        return nid
        
    def copyROI(self):
        ''' Copy current ROI. Offset from original for visibility '''
        osFract = 0.05
        if self.currentROIindex!=None:
            roi     = self.rois[self.currentROIindex]
            # For rectangular ROI, offset by a fraction of the rotated size
            if type(roi)==RectROIcustom: 
                roiState = roi.getState()
                pos      = roiState['pos']
                size     = roiState['size']
                angle    = roiState['angle']
                dx,dy    = np.array(size)*osFract               
                ang      = np.radians(angle)
                cosa     = np.cos(ang)
                sina     = np.sin(ang)
                dxt      = dx*cosa - dy*sina
                dyt      = dx*sina + dy*cosa
                offset   = QtCore.QPointF(dxt,dyt) 
                self.addROI(pos+offset,size,angle)
            # For a polyline ROI, offset by a fraction of the bounding rectangle
            if type(roi)==PolyLineROIcustom:                             
                br        = roi.shape().boundingRect()
                size      = np.array([br.width(),br.height()])
                osx,osy   = size * osFract
                offset    = QtCore.QPointF(osx,osy)                
                hps       = [i[-1] for i in roi.getSceneHandlePositions(index=None)]                
                hpsOffset = [self.mapSceneToView(hp)+offset for hp in hps] 
                self.addPolyLineROI(hpsOffset)
     
    def saveROI(self):
        ''' Save the highlighted ROI to file '''   
        if self.currentROIindex!=None:
            roi = self.rois[self.currentROIindex]
            fileName = QtGui.QFileDialog.getSaveFileName(None,self.tr("Save ROI"),QtCore.QDir.currentPath(),self.tr("ROI (*.roi)"))
            # Fix for PyQt/PySide compatibility. PyQt returns a QString, whereas PySide returns a tuple (first entry is filename as string)        
            if isinstance(fileName,types.TupleType): fileName = fileName[0]
            if hasattr(QtCore,'QString') and isinstance(fileName, QtCore.QString): fileName = str(fileName)            
            if not fileName=='':
                if type(roi)==RectROIcustom:
                    roiState = roi.saveState()
                    roiState['type']='RectROIcustom'
                elif type(roi)==PolyLineROIcustom: 
                    roiState = {}
                    hps   = [self.mapSceneToView(i[-1]) for i in roi.getSceneHandlePositions(index=None)]                                                      
                    hps   = [[hp.x(),hp.y()] for hp in hps]
                    roiState['type']='PolyLineROIcustom'    
                    roiState['handlePositions'] = hps
                pickle.dump( roiState, open( fileName, "wb" ) )
                          
    def loadROI(self):
        ''' Load a previously saved ROI from file '''
        fileNames = QtGui.QFileDialog.getOpenFileNames(None,self.tr("Load ROI"),QtCore.QDir.currentPath(),self.tr("ROI (*.roi)"))
        # Fix for PyQt/PySide compatibility. PyQt returns a QString, whereas PySide returns a tuple (first entry is filename as string)        
        if isinstance(fileNames,types.TupleType): fileNames = fileNames[0]
        if hasattr(QtCore,'QStringList') and isinstance(fileNames, QtCore.QStringList): fileNames = [str(i) for i in fileNames]
        if len(fileNames)>0:
            for fileName in fileNames:
                if fileName!='':
                    roiState = pickle.load( open(fileName, "rb") )
                    if roiState['type']=='RectROIcustom':
                        self.addROI(roiState['pos'],roiState['size'],roiState['angle'])    
                    elif roiState['type']=='PolyLineROIcustom':
                        self.addPolyLineROI(roiState['handlePositions'])
            
    def removeROI(self):
        ''' Delete the highlighted ROI '''
        if self.currentROIindex!=None:
            roi = self.rois[self.currentROIindex]
            self.rois.pop(self.currentROIindex)
            self.removeItem(roi)  
            self.setCurrentROIindex(None) 

    def toggleViewMode(self):
        ''' Toggles between NORMAL (Black/White) and DEXA mode (colour) '''
        if self.viewMode == self.NORMAL:
            viewMode = self.DEXA
        else:
            viewMode = self.NORMAL
        self.setViewMode(viewMode)             
        
    def setViewMode(self,viewMode):
        self.viewMode = viewMode
        self.updateView()

    def updateView(self):
        self.background.setBrush(fn.mkBrush(self.viewMode.lut[0]))
        self.background.show()
        if    self.img is None: return
        else: self.img.setLookupTable(self.viewMode.lut)            
       
    def showImage(self,arr):
        if arr is None: 
            self.img = None
            return
        if self.img is None: 
            self.img = pg.ImageItem(arr,autoRange=False,autoLevels=False)
            self.addItem(self.img)      
        self.img.setImage(arr,autoLevels=False)
        self.updateView()  
