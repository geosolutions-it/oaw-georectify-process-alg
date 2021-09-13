from unittest import mock
from geotiflib import utils


@mock.patch('os.name', 'nt')
def test_is_windows():
    assert utils.Utils.is_windows() is True


@mock.patch('os.name', 'posix')
def test_is_windows_false():
    assert utils.Utils.is_windows() is False


def test_set_gdal_tiff_mask():
    assert utils.Utils.set_gdal_tiff_mask() is True


def test_check_error_yes():
    check = utils.Utils.check_output("An error was occured")
    assert check[0] is False
    assert check[1] == "An error was occured"


def test_check_error_no():
    check = utils.Utils.check_output("Everything is ok")
    assert check[0] is True
    assert check[1] is None


def test_make_command():
    command = utils.Utils.make_command("gdalinfo", "-json", "-stats")
    assert command == ['gdalinfo', '-json', '-stats']
    command = utils.Utils.make_command("gdalwarp", "-overwrite", "-of VRT")
    assert command == ['gdalwarp', '-overwrite', '-of', 'VRT']


