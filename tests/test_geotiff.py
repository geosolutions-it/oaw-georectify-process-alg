import os
import mock
from geotiflib import geotiff
from .utils import get_data_folder


def test_constructor():
    tif = geotiff.GeoTiff("")
    assert isinstance(tif, geotiff.GeoTiff) is True


def test_info():
    path = os.path.join(get_data_folder(), "AC04078710.tif")
    tif = geotiff.GeoTiff(path)
    info = tif.info()
    assert ("Driver: GTiff/GeoTIFF" in info) is True


def test_metadata_existing():
    path = os.path.join(get_data_folder(), "AC04078710.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("TIFFTAG_RESOLUTIONUNIT")
    assert attribute == "2 (pixels/inch)"


def test_metadata_not_existing():
    path = os.path.join(get_data_folder(), "AC04078710.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("TIFFTAG_NOT_EXISTING")
    assert attribute is None


def test_is_processed():
    path = os.path.join(get_data_folder(), "AC04078710_grf_fin.tif")
    tif = geotiff.GeoTiff(path)
    assert tif.is_processed() is True


def test_is_processed_7mb():
    path = os.path.join(get_data_folder(), "AC04078710_7mb.tif")
    tif = geotiff.GeoTiff(path)
    assert tif.is_processed() is False
