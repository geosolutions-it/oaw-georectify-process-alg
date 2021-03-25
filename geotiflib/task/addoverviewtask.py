from .basetask import BaseTask


class AddOverviewTask(BaseTask):
    """
    This task will add overviews to the images
    gdaladdo -r average --config GDAL_TIFF_OVR_BLOCKSIZE 512 AC04078710_georef_final.tif
    """
    def run(self):
        pass
