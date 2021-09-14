import os
from .basetask import BaseTask
from ..gdalprocess import GdalProcess
from ..gdalcommand import GdalCommand


class SeparateBandTask(BaseTask):
    """
    Using the gdalbuildvrt tool we want to separate the 3 bands as 3 different VRT (Virtual Dataset) files
    Example of the command:
    gdalbuildvrt -b 1 -hidenodata AC04078710_georef_b1.vrt AC04078710_georef.tif
    gdalbuildvrt -b 2 -hidenodata AC04078710_georef_b2.vrt AC04078710_georef.tif
    gdalbuildvrt -b 3 -hidenodata AC04078710_georef_b3.vrt AC04078710_georef.tif
    """
    def __init__(self, *args, **kwargs):
        BaseTask.__init__(self, 'SEPARATE_BAND_TASK', *args, **kwargs)
        self._bands = 3

    def run(self):
        in_image = self._kwargs["input"]
        out_vrt = self._kwargs["output"]
        if os.path.exists(in_image) and os.path.isfile(in_image):
            for band in range(self._bands):
                gdal_prc = GdalProcess(GdalCommand.BUILD_VRT,
                                       '-b ' + str(band+1),
                                       '-hidenodata',
                                       out_vrt.replace("{band}", str(band+1)),
                                       in_image, ret_out=True, log_location=self._kwargs['log_location'])
                gdal_prc.process()
        else:
            raise FileNotFoundError(in_image)
