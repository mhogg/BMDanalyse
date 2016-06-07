==========
BMDanalyse
==========

.. image:: https://img.shields.io/pypi/v/bmdanalyse.svg
   :target: https://pypi.python.org/pypi/bmdanalyse/
   :alt: Latest PyPI version
   
.. image:: https://img.shields.io/pypi/dm/bmdanalyse.svg
   :target: https://pypi.python.org/pypi/bmdanalyse/
   :alt: Number of PyPI downloads

Copyright 2016, Michael Hogg (michael.christopher.hogg@gmail.com)

MIT license - See LICENSE.txt for details on usage and distribution

-----
About
-----

A graphical tool used for the regional analysis of a time series of 2D medical images. This was created for the analysis of virtual x-rays, created by companion tools `bonemapy`_ and `pyvXRAY`_ from the results of a computer simulation. Intended to be used to evaluate the bone gain / loss in a number of regions of interest (ROIs) over time, typically due to bone remodelling as a result of stress shielding around an orthopaedic implant.

Written in pure Python using PyQt/PySide, pyqtgraph, numpy, matplotlib and pillow. Should work on any platform, but has only been tested on Windows.

.. _bonemapy: https://github.com/mhogg/bonemapy
.. _pyvxray: https://github.com/mhogg/pyvxray

------------
Requirements
------------

* Python 2.7
* PyQt >= 4.11
* pyqtgraph >= 0.9.10
* numpy >= 1.9
* matplotlib >= 1.4
* pillow >= 3.0

**NOTE:** All these requirements are available within the Anaconda Python distribution

--------------------
Instructions for use
--------------------

- Load a time series of 2D medical images (in image format such as bmp, png etc). All images should be grayscale and of the same size.
- Use the up / down arrows in the Image toolbox to place the images in chronological order. A time series of virtual X-rays is provided in the sampleMedicalImages directory. 
- Create some Regions of Interest (ROIs) and run the ROI analysis tool from the Analysis toolbox. A plot will be generated showing the change in the average grayscale value with each ROI over time.
- Run the Image analysis tool from the Analysis toolbox. A contour will be displayed, showing regions of bone loss in blue and bone gain in red.
