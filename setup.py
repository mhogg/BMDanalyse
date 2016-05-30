
#from ez_setup import use_setuptools
#use_setuptools()
#import setuptools
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup
import BMDanalyse

setup(
    name = 'BMDanalyse',
    version = BMDanalyse.__version__,
    description = 'Tool to analyse regional changes in a time series of 2D medical images.',
    license = 'MIT license',
    keywords = ["python,medical,image,analysis,ROIs,xray"],    
    author = 'Michael Hogg',
    author_email = 'michael.christopher.hogg@gmail.com',
    url = "http://pypi.python.org/pypi/BMDanalyse/",
    download_url = "https://pypi.python.org/packages/source/B/BMDanalyse/BMDanalyse-%s.zip" % BMDanalyse.__version__,
    packages = ['BMDanalyse'],
    package_data = {'BMDanalyse': ['icons/*','changeLog.txt',
                                   'sampleMedicalImages/Implant/XYplane/*',
                                   'sampleMedicalImages/Implant/YZplane/*', 
                                   'sampleMedicalImages/No implant/XYplane/*',
                                   'sampleMedicalImages/No implant/YZplane/*']},
    entry_points = { 'console_scripts': ['BMDanalyse = BMDanalyse.BMDanalyse:run',]},
    classifiers = [
        "Programming Language :: Python",                                  
        "Programming Language :: Python :: 2", 
        "Programming Language :: Python :: 2.6",    
        "Programming Language :: Python :: 2.7",                                                    
        "Development Status :: 4 - Beta",                                  
        "Environment :: Other Environment", 
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",   
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",     
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Visualization",
        ],
    long_description = """
About
-----

A tool used for the regional analysis of a time series of 2D medical images, typically X-rays or virtual X-rays (output from a computer simulation, such as those created using `pyvXRAY <http://pypi.python.org/pypi/pyvxray>`_).
Intended to be used to evaluate the bone gain / loss in a number of regions of interest (ROIs) over time, typically due to bone remodelling as a result of stress shielding around an orthopaedic implant.
    
Written in pure Python using PyQt4/PySide, pyqtgraph, numpy, PIL and matplotlib. Should work on any platform, but has only been tested on Windows.

How to use
----------

 - Load a time series of 2D medical images (in image format such as bmp, png etc). 
 - Use the up / down arrows below the image file list to place the images in chronological order. A time series of virtual X-rays is provided in the sampleMedicalImages directory. 
 - Create some Regions of Interest (ROIs) and run the ROI analysis tool from the Analyse option on the main toolbar
 - Run the Image analysis tool from the Analyse option on the main toolbar
""",

    install_requires = [
        'pyqtgraph',        
        'matplotlib',
        'numpy',
        'pillow',
        ],
)
