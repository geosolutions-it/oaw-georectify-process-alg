import os
from .basetask import BaseTask
from ..gdalprocess import GdalProcess
from ..gdalcommand import GdalCommand


class WarpTask(BaseTask):
    """
    This task will warp the raster tif file
    Example of the command:
    gdalwarp -t_srs EPSG:3857 -r lanczos -tps -co -dstalpha  AC04078710_gcp.tif AC04078710_georef.tif
    """
    def __init__(self, *args, **kwargs):
        BaseTask.__init__(self, 'WARP_TASK', *args, **kwargs)
        self._epsg = 3857

    def run(self):
        in_image = self._kwargs["input"]
        out_image = self._kwargs["output"]
        if os.path.exists(in_image) and os.path.isfile(in_image):
            gdal_prc = GdalProcess(GdalCommand.WARP,
                                   '-t_srs EPSG:' + str(self._epsg) + ' -r lanczos -tps -co -dstalpha',
                                   in_image, out_image, ret_out=True)
            result = gdal_prc.process()
        else:
            raise FileNotFoundError(in_image)
