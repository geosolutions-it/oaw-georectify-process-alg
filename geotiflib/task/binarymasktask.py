import os
from .basetask import BaseTask
from ..gdalprocess import GdalProcess
from ..gdalcommand import GdalCommand


class BinaryMaskTask(BaseTask):
    """
    This task will create the binary mask
    Example of the command:
    gdal_calc.py --type=Byte --creation-option=NUM_THREADS=4 --creation-option=PHOTOMETRIC=MINISBLACK
    --creation-option=NBITS=1 --creation-option=TILED=YES --creation-option=COMPRESS=DEFLATE
    -A AC04078710_georef_b1.vrt -B AC04078710_georef_b2.vrt -C AC04078710_georef_b3.vrt
    --calc="logical_not(logical_and(logical_and(A==0,B==0),C==0))"
     --outfile AC04078710_georef.msk.tif
    """
    def __init__(self, *args, **kwargs):
        BaseTask.__init__(self, 'BINARY_MASK_TASK', *args, **kwargs)
        self._bands = 3
        self._letters = ['A', 'B', 'C']
        self._threads = 4

    def run(self):
        in_vrt = self._kwargs["input"]
        out_image = self._kwargs["output"]
        vrt_files = []
        for band in range(self._bands):
            vrt_file = in_vrt.replace("{band}", str(band+1))
            if os.path.exists(vrt_file) and os.path.isfile(vrt_file):
                vrt_files.append('-' + self._letters[band] + ' ' + vrt_file)
            else:
                raise FileNotFoundError(vrt_file)

        gdal_prc = GdalProcess(GdalCommand.CALC,
                               '--type=Byte',
                               '--co=NUM_THREADS=' + str(self._threads),
                               '--co=PHOTOMETRIC=MINISBLACK',
                               '--co=NBITS=1',
                               '--co=TILED=YES',
                               '--co=COMPRESS=DEFLATE',
                               ' '.join(vrt_files),
                               '--calc=logical_not(logical_and(logical_and(A==0,B==0),C==0))',
                               '--outfile ' + out_image, ret_out=True)
        gdal_prc.process()
