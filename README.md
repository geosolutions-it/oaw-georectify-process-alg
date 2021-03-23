# oaw-georectify-process-alg
Alghorithms library to process raster images using gdal


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