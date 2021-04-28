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


def test_metadata_oaw_creator():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("OAW_CREATOR")
    assert attribute == "\\xc3\\x96sterreichische Akademie der Wissenschaften Wien"


def test_metadata_oaw_date():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("OAW_DATE")
    assert attribute == "1750"


def test_metadata_oaw_description():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("OAW_DESCRIPTION")
    assert "Bibliographische Informationen Quelle;" in attribute and "Augsburg [Verlagsort]" in attribute


def test_metadata_oaw_edition():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("OAW_EDITION")
    assert attribute == ""


def test_metadata_oaw_format():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("OAW_FORMAT")
    assert attribute == "Massstab: 24000000"


def test_metadata_oaw_identifier():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("OAW_IDENTIFIER")
    assert attribute == "AC12706659"


def test_metadata_oaw_relation():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("OAW_RELATION")
    assert attribute == "Gesamttitel: Accurata Globi Terrestris; Reihenfolge in Serie: [2]"


def test_metadata_oaw_source():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("OAW_SOURCE")
    assert attribute == "https://goobi.acdh.oeaw.ac.at/viewer/image/AC12706659"


def test_metadata_oaw_subject():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("OAW_SUBJECT")
    assert attribute == "Kartentyp; Kontinentalkarte"


def test_metadata_oaw_title():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.metadata("OAW_TITLE")
    assert attribute == "SEUTTER Europa 1750"


def test_is_processed():
    path = os.path.join(get_data_folder(), "AC04078710_grf_fin.tif")
    tif = geotiff.GeoTiff(path)
    assert tif.is_processed() is True


def test_is_processed_colorinterp_is_undefined():
    path = os.path.join(get_data_folder(), "AC04078710_colorinterp_is_undefined.tif")
    tif = geotiff.GeoTiff(path)
    assert tif.is_processed() is False


def test_is_processed_no_overviews():
    path = os.path.join(get_data_folder(), "AC04078710_no_overviews.tif")
    tif = geotiff.GeoTiff(path)
    assert tif.is_processed() is True


def test_xmp_metadata_date():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.xmp_metadata(geotiff.XmlTags.XMP_DATE)
    assert attribute == '1750'


def test_xmp_metadata_creator():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.xmp_metadata(geotiff.XmlTags.XMP_CREATOR)
    assert attribute == '\\xc3\\x96sterreichische Akademie der Wissenschaften Wien'


def test_xmp_metadata_description():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.xmp_metadata(geotiff.XmlTags.XMP_DESCRIPTION)
    assert 'Bibliographische Informationen Quelle' in attribute  and 'Augsburg [Verlagsort]' in attribute


def test_xmp_metadata_format():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.xmp_metadata(geotiff.XmlTags.XMP_FORMAT)
    assert attribute == 'Massstab: 37000000'


def test_xmp_metadata_identifier():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.xmp_metadata(geotiff.XmlTags.XMP_IDENTIFIER)
    assert attribute == 'AC12708841'


def test_xmp_metadata_relation():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.xmp_metadata(geotiff.XmlTags.XMP_RELATION)
    assert attribute == 'Gesamttitel: Accurata Globi Terrestris; Reihenfolge in Serie: [5]'


def test_xmp_metadata_source():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.xmp_metadata(geotiff.XmlTags.XMP_SOURCE)
    assert attribute == 'https://goobi.acdh.oeaw.ac.at/viewer/image/AC12708841'


def test_xmp_metadata_subject():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.xmp_metadata(geotiff.XmlTags.XMP_SUBJECT)
    assert attribute == 'Kartentyp; Kontinentalkarte'


def test_xmp_metadata_title():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.xmp_metadata(geotiff.XmlTags.XMP_TITLE)
    assert attribute == 'SEUTTER Suedamerika 1750'


def test_xmp_metadata_title_str():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.xmp_metadata("title")
    assert attribute == 'SEUTTER Suedamerika 1750'
    attribute = tif.xmp_metadata("TITLE")
    assert attribute == 'SEUTTER Suedamerika 1750'


def test_xmp_metadata_dict():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    dictionary = tif.xmp_metadata_dict()
    assert dictionary["creator"] == '\\xc3\\x96sterreichische Akademie der Wissenschaften Wien'
    assert dictionary["date"] == '1750'
    assert 'Bibliographische Informationen Quelle' \
           in dictionary["description"] and 'Augsburg [Verlagsort]' in dictionary["description"]
    assert dictionary["format"] == 'Massstab: 37000000'
    assert dictionary["identifier"] == 'AC12708841'
    assert dictionary["relation"] == 'Gesamttitel: Accurata Globi Terrestris; Reihenfolge in Serie: [5]'
    assert dictionary["source"] == 'https://goobi.acdh.oeaw.ac.at/viewer/image/AC12708841'
    assert dictionary["subject"] == 'Kartentyp; Kontinentalkarte'
    assert dictionary["title"] == 'SEUTTER Suedamerika 1750'
    assert dictionary["edition"] is None


def test_oaw_metadata_title():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    attribute = tif.oaw_metadata(geotiff.XmlTags.XMP_TITLE)
    assert attribute == "SEUTTER Europa 1750"
    attribute = tif.oaw_metadata("OAW_TITLE")
    assert attribute == "SEUTTER Europa 1750"


def test_oaw_metadata_dict_01():
    path = os.path.join(get_data_folder(), "test999_0007.tif")
    tif = geotiff.GeoTiff(path)
    dictionary = tif.oaw_metadata_dict()
    assert dictionary["creator"] == '\\xc3\\x96sterreichische Akademie der Wissenschaften Wien'
    assert dictionary["date"] == '1750'
    assert 'Bibliographische Informationen Quelle' \
           in dictionary["description"] and 'Augsburg [Verlagsort]' in dictionary["description"]
    assert dictionary["format"] == 'Massstab: 37000000'
    assert dictionary["identifier"] == 'AC12708841'
    assert dictionary["relation"] == 'Gesamttitel: Accurata Globi Terrestris; Reihenfolge in Serie: [5]'
    assert dictionary["source"] == 'https://goobi.acdh.oeaw.ac.at/viewer/image/AC12708841'
    assert dictionary["subject"] == 'Kartentyp; Kontinentalkarte'
    assert dictionary["title"] == 'SEUTTER Suedamerika 1750'
    assert dictionary["edition"] is None


def test_oaw_metadata_dict_02():
    path = os.path.join(get_data_folder(), "output_with_oaw_meta.tif")
    tif = geotiff.GeoTiff(path)
    dictionary = tif.oaw_metadata_dict()
    assert dictionary["creator"] == '\\xc3\\x96sterreichische Akademie der Wissenschaften Wien'
    assert dictionary["date"] == '1750'
    assert 'Bibliographische Informationen Quelle' \
           in dictionary["description"] and 'Augsburg [Verlagsort]' in dictionary["description"]
    assert dictionary["format"] == 'Massstab: 24000000'
    assert dictionary["identifier"] == 'AC12706659'
    assert dictionary["relation"] == 'Gesamttitel: Accurata Globi Terrestris; Reihenfolge in Serie: [2]'
    assert dictionary["source"] == 'https://goobi.acdh.oeaw.ac.at/viewer/image/AC12706659'
    assert dictionary["subject"] == 'Kartentyp; Kontinentalkarte'
    assert dictionary["title"] == 'SEUTTER Europa 1750'
    assert dictionary["edition"] is None