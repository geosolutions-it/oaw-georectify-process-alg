import os
from .basetask import BaseTask
from ..gdalprocess import GdalProcess
from ..gdalcommand import GdalCommand


class AddOverviewTask(BaseTask):
    """
    This task will add overviews to the images
    gdaladdo -r average --config GDAL_TIFF_OVR_BLOCKSIZE 512 AC04078710_georef_final.tif
    """
    def __init__(self, *args, **kwargs):
        BaseTask.__init__(self, 'ADD_OVERVIEW_TASK', *args, **kwargs)
        self._block_size = 512

    def run(self):
        in_tif = self._kwargs["input"]

        if not os.path.exists(in_tif) or not os.path.isfile(in_tif):
            raise FileNotFoundError(in_tif)

        gdal_prc = GdalProcess(GdalCommand.ADDO,
                               '-r average',
                               '--config GDAL_TIFF_OVR_BLOCKSIZE %s' % self._block_size,
                               in_tif,
                               ret_out=True, log_location=self._kwargs['log_location'])
        gdal_prc.process()
