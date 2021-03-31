# oaw-georectify-process-alg
Alghorithms library to process raster images using osgeo/gdal

This plugin requires to be runned in a QGIS environment

## Configure Environment variables
### Windows
This is an example how to configure environment variables on Windows
PYTHONUNBUFFERED=1;
PATH=C:\OSGeo4W64\apps\qgis\bin\;C:\OSGeo4W64\apps\Python37\;C:\OSGeo4W64\apps\Python37\Scripts\;C:\OSGeo4W64\apps\qt5\bin\;C:\OSGeo4W64\apps\Python37\Scripts\;C:\OSGeo4W64\bin\;C:\Windows\;C:\Windows\system32\WBem\;C:\OSGeo4W64\apps\qgis\python\plugins;
OSGEO4W_ROOT=C:\OSGeo4W64;
PYTHONHOME=C:\OSGeo4W64\apps\Python37;
QGIS_PREFIX_PATH=C:\OSGeo4W64\apps\qgis;
QT_PLUGIN_PATH=C:\OSGeo4W64\apps\qgis\qtplugins\;C:\OSGeo4W64\apps\qt5\plugins;
PYTHONPATH=C:\OSGeo4W64\apps\qgis\python;
GDAL_DATA=C:\OSGeo4W64\share\gdal;
PROJ_LIB=C:\OSGeo4W64\share\proj

## Running tests
> python setup.py pytest

will execute all tests stored in the "tests" folder.

## Building the library
> python setup.py bdist_wheel

The wheel file will be created in the "dist" folder. 

## Installing the library
> pip install ./dist/geotiflib-<version>-py3-none-any.whl

where:
- \<version\>: is the version of the library (eg. 0.1.0)

## Usage
```
from geotiflib import utils
utils.Utils.is_windows()
```