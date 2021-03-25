import json
from .gdalprocess import GdalProcess
from .gdalcommand import GdalCommand


class GeoTiff:

    def __init__(self, path):
        """
        Constructor
        :param path: full path to the TIF image
        """
        self._path = path
        self._info = None

    def info(self):
        """
        Read information from the GeoTiff using the gdalinfo utility
        Return the complete information as string
        :return: string
        """
        prc = GdalProcess(GdalCommand.INFO, self._path, ret_out=True)
        self._info = str(prc.process())
        return self._info

    def metadata(self, name):
        """
        Return the value of a specific metadata information
        :param name: name of the metadata of interest
        :return: string
        """
        try:
            if self._info is None:
                self.info()
            if name in self._info:
                parts = self._info.split(name + "=")
                return parts[1].split(r"\r")[0]
        finally:
            pass
        return None