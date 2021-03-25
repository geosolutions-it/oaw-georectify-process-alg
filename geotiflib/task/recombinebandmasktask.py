import os
from .basetask import BaseTask
from ..gdalprocess import GdalProcess
from ..gdalcommand import GdalCommand


class RecombineBandMaskTask(BaseTask):
    """
    This task will recombine the 3 bands with the mask band
    gdalbuildvrt -separate
        AC04078710_georef_final.vrt
        AC04078710_georef_b1.vrt
        AC04078710_georef_b2.vrt
        AC04078710_georef_b3.vrt
        AC04078710_georef.msk.tif
    """
    def __init__(self, *args, **kwargs):
        BaseTask.__init__(self, 'RECOMBINE_BAND_MASK_TASK', *args, **kwargs)
        self._bands = 3

    def run(self):
        in_vrt = self._kwargs["input_vrt"]
        in_mask = self._kwargs["input_mask"]
        out_vrt = self._kwargs["output"]

        in_files = []
        for band in range(self._bands):
            in_files.append(in_vrt.replace("{band}", str(band+1)))
        in_files.append(in_mask)

        for file in in_files:
            if not os.path.exists(file) or not os.path.isfile(file):
                raise FileNotFoundError(file)

        gdal_prc = GdalProcess(GdalCommand.BUILD_VRT, '-separate',
                               out_vrt,
                               in_files[0],
                               in_files[1],
                               in_files[2],
                               in_files[3],
                               ret_out=True)
        gdal_prc.process()
