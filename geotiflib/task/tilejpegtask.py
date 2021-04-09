import os
from .basetask import BaseTask
from ..gdalprocess import GdalProcess
from ..gdalcommand import GdalCommand


class TileJpegTask(BaseTask):
    """
    This task will restrutcure the image in tiled way and use JPEG compression
    gdal_translate -mo "NODATA_VALUES=0 0 0" -CO "COMPRESS=JPEG" -CO "PHOTOMETRIC=YCBCR" -CO "TILED=YES"
        -CO BLOCKXSIZE=512 -CO BLOCKYSIZE=512
        -b 1 -b 2 -b 3 -mask 4
        AC04078710_georef_final.vrt AC04078710_georef_final.tif
    """
    def __init__(self, *args, **kwargs):
        BaseTask.__init__(self, 'TILE_JPEG_TASK', *args, **kwargs)
        self._block_size = 512

    def run(self):
        in_vrt = self._kwargs["input"]
        out_tif = self._kwargs["output"]

        if not os.path.exists(in_vrt) or not os.path.isfile(in_vrt):
            raise FileNotFoundError(in_vrt)
        # '-mo "NODATA_VALUES=0|0|0"',
        gdal_prc = GdalProcess(GdalCommand.TRANSLATE,
                               '-mo NODATA_VALUES=0|0|0',
                               '-colorinterp red,green,blue',
                               '-co COMPRESS=JPEG',
                               '-co PHOTOMETRIC=YCBCR',
                               '-co TILED=YES',
                               '-co BLOCKXSIZE=%s' % str(self._block_size),
                               '-co BLOCKYSIZE=%s' % str(self._block_size),
                               "-b 1", "-b 2", "-b 3", "-mask 4",
                               in_vrt,
                               out_tif,
                               ret_out=True)
        gdal_prc.process()

