#BMDanalyse

**Graphical tool to analyse regional changes in a time series of 2D medical images**

[![PyPi version](https://img.shields.io/pypi/v/bmdanalyse.svg)](https://pypi.python.org/pypi/bmdanalyse/)
[![PyPi downloads](https://img.shields.io/pypi/dm/bmdanalyse.svg)](https://pypi.python.org/pypi/bmdanalyse/)

Copyright 2013, Michael Hogg (michael.christopher.hogg@gmail.com)

MIT license - See LICENSE.txt for details on usage and distribution

## About

A graphical tool used for the regional analysis of a time series of 2D medical images. This was created for the analysis of virtual x-rays, created by companion tools [bonemapy](https://github.com/mhogg/bonemapy) and [pyvXRAY](https://github.com/mhogg/pyvxray) from the results of a computer simulation. Intended to be used to evaluate the bone gain / loss in a number of regions of interest (ROIs) over time, typically due to bone remodelling as a result of stress shielding around an orthopaedic implant.

Written in pure Python using PyQt/PySide, pyqtgraph, numpy, matplotlib and pillow. Should work on any platform, but has only been tested on Windows.

## Requirements

* Python 2.7
* PyQt >= 4.11
* pyqtgraph >= 0.9.10
* numpy >= 1.9
* matplotlib >= 1.4
* pillow >= 3.0

**NOTES:**

1.  All these requirements are available within the Anaconda Python distribution
