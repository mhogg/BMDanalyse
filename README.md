#BMDanalyse

**Graphical tool to analyse regional changes in a time series of 2D medical images**

Copyright 2013, Michael Hogg (michael.christopher.hogg@gmail.com)

MIT license - See LICENSE.txt for details on usage and distribution

## About

A graphical tool used for the regional analysis of a time series of 2D medical images. This was created for the analysis of virtual x-rays, created by companion tool [pyvXRAY](https://github.com/mhogg/pyvxray) from the results of a computer simulation. Intended to be used to evaluate the bone gain / loss in a number of regions of interest (ROIs) over time, typically due to bone remodelling as a result of stress shielding around an orthopaedic implant.

Written in pure Python using PyQt4/PySide, pyqtgraph, numpy, PIL and matplotlib. Should work on any platform, but has only been tested on Windows.

## Requirements

### Software requirements

* Python >= 2.6
* pyQtGraph >= v0.9.7
* PyQt4 >= 4.9.7 or PySide >= 1.1
* numpy >= 1.4
* matplotlib >= 1.0
* Python Imaging Library (PIL) >= v1.1.6

**NOTES:**

1.  All these requirements are available within the Enthought Canopy or Anaconda Python distributions
2.  Some issues with window zoom when using Python 2.6. These will be fixed in the next release of pyQtGraph
