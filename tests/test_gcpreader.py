import os
import mock
from geotiflib import gcpreader
from .utils import get_data_folder


def test_constructor():
    reader = gcpreader.GCPReader("")
    assert isinstance(reader, gcpreader.GCPReader) is True


def test_parse():
    reader = gcpreader.GCPReader(os.path.join(get_data_folder(), "AC04078710.tif.points"))
    assert reader.parse() is True


def test_count_all():
    reader = gcpreader.GCPReader(os.path.join(get_data_folder(), "AC04078710.tif.points"))
    reader.parse()
    assert reader.count(only_enabled=False) == 26


def test_count_enabled():
    reader = gcpreader.GCPReader(os.path.join(get_data_folder(), "AC04078710.tif.points"))
    reader.parse()
    assert reader.count(only_enabled=True) == 24


def test_gcp_str():
    row = ['1822331.48124592285603285', '6141557.76140719745308161',
           '8540.91993957704107743', '-4987.66937311178116943',
           '0', '0.00000000323416316', '0.00000000122599886', '0.00000000345874031']
    gcp = gcpreader.GCP(row)
    assert str(gcp) == "-gcp 8540.92 4987.67 1822331.48 6141557.76"


def test_get_list():
    reader = gcpreader.GCPReader(os.path.join(get_data_folder(), "AC04078710.tif.points"))
    reader.parse()
    items = reader.get_list(only_enabled=True)
    assert len(items) == 24


def test_get_list_as_string():
    reader = gcpreader.GCPReader(os.path.join(get_data_folder(), "AC04078710.tif.points"))
    reader.parse()
    string = reader.get_list_as_string(only_enabled=True)
    assert "-gcp 16841.09 8996.47 2905721.28 5531134.15 -gcp 11247.94 12303.93 2171092.52 5171439.50" in string
