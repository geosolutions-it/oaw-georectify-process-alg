from .basetask import BaseTask


class TileJpegTask(BaseTask):
    """
    This task will restrutcure the image in tiled way and use JPEG compression
    gdal_translate -mo "NODATA_VALUES=0 0 0" -CO "COMPRESS=JPEG" -CO "PHOTOMETRIC=YCBCR" -CO "TILED=YES"
        -CO BLOCKXSIZE=512 -CO BLOCKYSIZE=512
        -b 1 -b 2 -b 3 -mask 4
        AC04078710_georef_final.vrt AC04078710_georef_final.tif
    """
    def run(self):
        pass

