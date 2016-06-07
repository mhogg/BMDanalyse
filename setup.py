from setuptools import setup
from codecs import open
from os import path

# get current path
here = path.abspath(path.dirname(__file__))

# function to open the readme file
def readme():
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        return f.read()
        
# find the version
exec(open(path.join('BMDanalyse','version.py')).read())

setup(
    name = 'BMDanalyse',
    version = __version__,
    description = 'Tool to analyse regional changes in a time series of 2D medical images.',
    long_description = readme(),
    license = 'MIT license',
    keywords = ["python,medical,image,analysis,ROIs,xray"],    
    author = 'Michael Hogg',
    author_email = 'michael.christopher.hogg@gmail.com',
    url = "http://pypi.python.org/pypi/BMDanalyse/",
    download_url = "https://pypi.python.org/packages/source/B/BMDanalyse/BMDanalyse-%s.zip" % __version__,
    packages = ['BMDanalyse'],
    package_data = {'BMDanalyse': ['icons/*','changeLog.txt',
                                   'sampleMedicalImages/Implant/XYplane/*',
                                   'sampleMedicalImages/Implant/YZplane/*', 
                                   'sampleMedicalImages/No implant/XYplane/*',
                                   'sampleMedicalImages/No implant/YZplane/*']},
    entry_points = { 'console_scripts': ['BMDanalyse = BMDanalyse.BMDanalyse:run',]},
    install_requires = ['pyqtgraph','matplotlib','numpy','pillow',],
    classifiers = [
        "Programming Language :: Python",                                  
        "Programming Language :: Python :: 2",
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
)
