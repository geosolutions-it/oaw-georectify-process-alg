import codecs
from urllib.parse import unquote
from enum import Enum
from .utils import Utils
from .gdalprocess import GdalProcess
from .gdalcommand import GdalCommand


class XmlTag:
    def __init__(self, open_tag, close_tag, key):
        self.open = open_tag
        self.close = close_tag
        self.key = key


class XmlTags(Enum):
    XMP_CREATOR = XmlTag("<dc:creator><rdf:Seq><rdf:li>", "</rdf:li></rdf:Seq></dc:creator>", "OAW_CREATOR")
    XMP_DATE = XmlTag("<dc:date><rdf:Seq><rdf:li>", "</rdf:li></rdf:Seq></dc:date>", "OAW_DATE")
    XMP_DESCRIPTION = XmlTag("<dc:description><rdf:Alt><rdf:li xml:lang='x-default'>", "</rdf:li></rdf:Alt></dc:description>", "OAW_DESCRIPTION")
    XMP_FORMAT = XmlTag("<dc:format>", "</dc:format>", "OAW_FORMAT")
    XMP_IDENTIFIER = XmlTag("<dc:identifier>", "</dc:identifier>", "OAW_IDENTIFIER")
    XMP_RELATION = XmlTag("<dc:relation><rdf:Bag><rdf:li>", "</rdf:li></rdf:Bag></dc:relation>", "OAW_RELATION")
    XMP_SOURCE = XmlTag("<dc:source>", "</dc:source>", "OAW_SOURCE")
    XMP_SUBJECT = XmlTag("<dc:subject><rdf:Bag><rdf:li>", "</rdf:li></rdf:Bag></dc:subject>", "OAW_SUBJECT")
    XMP_TITLE = XmlTag("<dc:title><rdf:Alt><rdf:li xml:lang='x-default'>", "</rdf:li></rdf:Alt></dc:title>", "OAW_TITLE")
    XMP_EDITION = XmlTag("<???>", "</???>", "OAW_EDITION")

    @staticmethod
    def xmp_from_string(tag_name):
        name = tag_name.lower()
        if name == 'creator':
            return XmlTags.XMP_CREATOR
        elif name == 'date':
            return XmlTags.XMP_DATE
        elif name == 'description':
            return XmlTags.XMP_DESCRIPTION
        elif name == 'format':
            return XmlTags.XMP_FORMAT
        elif name == 'identifier':
            return XmlTags.XMP_IDENTIFIER
        elif name == 'relation':
            return XmlTags.XMP_RELATION
        elif name == 'source':
            return XmlTags.XMP_SOURCE
        elif name == 'subject':
            return XmlTags.XMP_SUBJECT
        elif name == 'title':
            return XmlTags.XMP_TITLE
        elif name == 'edition':
            return XmlTags.XMP_EDITION
        else:
            return None


class GeoTiff:

    def __init__(self, path):
        """
        Constructor
        :param path: full path to the TIF image
        """
        self._path = path
        self._info = None
        self._xmp_xml = None

    def info(self):
        """
        Read information from the GeoTiff using the gdalinfo utility
        Return the complete information as string
        :return: string
        """
        prc = GdalProcess(GdalCommand.INFO, self._path, ret_out=True)
        self._info = str(prc.process())
        return self._info

    def is_processed(self):
        """
        Check if the image is already optimized
        :return:
        """
        info = self.info()
        if "Overviews:" not in info:
            print("WARNING: the image does not contain overviews layers!")
        return "COMPRESSION=YCbCr JPEG" in info \
            and "Corner Coordinates:" in info \
            and "Band 1 Block=512x512 Type=Byte, ColorInterp=Red" in info \
            and "Band 2 Block=512x512 Type=Byte, ColorInterp=Green" in info \
            and "Band 3 Block=512x512 Type=Byte, ColorInterp=Blue" in info

    def metadata(self, tag, to_unquote=True):
        """
        Return the value of a specific metadata information
        :param tag: name (str or XmlTag) of the metadata of interest
        :return: string
        """
        try:
            if self._info is None:
                self.info()

            name = tag
            if not isinstance(tag, str):
                name = tag.value.key

            if name in self._info:
                parts = self._info.split(name + "=")
                if Utils.is_windows():
                    value = parts[1].split(r"\r")[0].replace("\\\\", "\\")
                else:
                    value = parts[1].split(r"\n")[0].replace("\\\\", "\\")
                if value.startswith('"'):
                    value = value[1:]
                if value.endswith('"'):
                    value = value[:-1]
                value = unquote(value)
                value = codecs.escape_decode(value)[0].decode()
                if not to_unquote:
                    value = value.replace("&amp;", "&")
                return value
        finally:
            pass
        return None

    def xmp_metadata(self, tag, to_unquote=True):
        if self._xmp_xml is None:
            with open(self._path, "rb") as fin:
                img = fin.read()
                img_as_string = str(img)
                xmp_start = img_as_string.find('<x:xmpmeta')
                xmp_end = img_as_string.find('</x:xmpmeta')
                if xmp_start != xmp_end:
                    self._xmp_xml = img_as_string[xmp_start:xmp_end + 12]\
                        .replace("/\\'", "'")\
                        .replace("\\'", "'")\
                        .replace("\\n", "")\
                        .replace("    ", " ")\
                        .replace("   ", " ")\
                        .replace("  ", " ")\
                        .replace("> <", "><")\
                        .replace("+", " ")
        if self._xmp_xml is not None:
            if isinstance(tag, str):
                tag = XmlTags.xmp_from_string(tag)
            tag_start = self._xmp_xml.find(tag.value.open)
            tag_end = self._xmp_xml.find(tag.value.close)
            if tag_start != tag_end:
                value = self._xmp_xml[tag_start+len(tag.value.open):tag_end]
                value = unquote(value)
                value = codecs.escape_decode(value)[0].decode()
                if not to_unquote:
                    value = value.replace("&amp;", "&")
                return value
        return None

    def xmp_metadata_dict(self):
        return {
            'creator': self.xmp_metadata(XmlTags.XMP_CREATOR),
            'date': self.xmp_metadata(XmlTags.XMP_DATE),
            'description': self.xmp_metadata(XmlTags.XMP_DESCRIPTION),
            'format': self.xmp_metadata(XmlTags.XMP_FORMAT),
            'identifier': self.xmp_metadata(XmlTags.XMP_IDENTIFIER),
            'relation': self.xmp_metadata(XmlTags.XMP_RELATION),
            'source': self.xmp_metadata(XmlTags.XMP_SOURCE),
            'subject': self.xmp_metadata(XmlTags.XMP_SUBJECT, False),
            'title': self.xmp_metadata(XmlTags.XMP_TITLE),
            'edition': self.xmp_metadata(XmlTags.XMP_EDITION)
        }

    def oaw_metadata(self, tag, to_uncode=True):
        value = self.metadata(tag)
        if value == "" or value is None:
            value = self.xmp_metadata(tag, to_uncode)
        return value

    def oaw_metadata_dict(self):
        return {
            'creator': self.oaw_metadata(XmlTags.XMP_CREATOR),
            'date': self.oaw_metadata(XmlTags.XMP_DATE),
            'description': self.oaw_metadata(XmlTags.XMP_DESCRIPTION),
            'format': self.oaw_metadata(XmlTags.XMP_FORMAT),
            'identifier': self.oaw_metadata(XmlTags.XMP_IDENTIFIER),
            'relation': self.oaw_metadata(XmlTags.XMP_RELATION),
            'source': self.oaw_metadata(XmlTags.XMP_SOURCE),
            'subject': self.oaw_metadata(XmlTags.XMP_SUBJECT, False),
            'title': self.oaw_metadata(XmlTags.XMP_TITLE),
            'edition': self.oaw_metadata(XmlTags.XMP_EDITION)
        }
