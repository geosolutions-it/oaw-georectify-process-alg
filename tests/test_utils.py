import mock
from geotiflib import utils


@mock.patch('os.name', 'nt')
def test_is_windows():
    assert utils.Utils.is_windows() is True


@mock.patch('os.name', 'posix')
def test_is_windows_false():
    assert utils.Utils.is_windows() is False


def test_set_gdal_tiff_mask():
    assert utils.Utils.set_gdal_tiff_mask() is True

