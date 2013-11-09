#BMDanalyse

**Graphical tool to analyse regional changes in a time series of 2D medical images**

Copyright 2013, Michael Hogg (michael.christopher.hogg@gmail.com)

MIT license - See LICENSE.txt for details on usage and distribution

## About

A graphical tool used for the regional analysis of a time series of 2D medical images. This was created for the analysis of virtual x-rays, created by companion tool [pyvXRAY](https://github.com/mhogg/pyvxray) from the results of a computer simulation. Intended to be used to evaluate the bone gain / loss in a number of regions of interest (ROIs) over time, typically due to bone remodelling as a result of stress shielding around an orthopaedic implant.

Written in pure Python using PyQt/PySide, pyqtgraph, numpy, matplotlib and PIL. Should work on any platform, but has only been tested on Windows.

## Requirements

* Python 2.6, 2.7
* PyQtGraph >= 0.9.7
* PyQt >= 4.9.7 or PySide >= 1.1
* numpy >= 1.4
* matplotlib >= 1.0
* Python Imaging Library (PIL) >= 1.1.7 OR Pillow >= 2.2.0

**NOTES:**

1.  All these requirements, with the exception of PyQtGraph, are available within the Enthought Canopy or Anaconda Python distributions
2.  Some issues with window zoom when using Python 2.6. These have been fixed in the PyQtGraph master repository
