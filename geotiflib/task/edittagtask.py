import os
import html
from .basetask import BaseTask
from ..gdalprocess import GdalProcess
from ..gdalcommand import GdalCommand
from ..geotiff import GeoTiff


class EditTagTask(BaseTask):
    """
    This task will add custom tags in the final image
    Example of the command:
    gdal_edit.py -mo OAW_CREATOR="The Author" final.tif
    """
    def __init__(self, *args, **kwargs):
        BaseTask.__init__(self, 'EDIT_TAG_TASK', *args, **kwargs)

    def run(self):
        in_tif = self._kwargs["input"]
        out_tif = self._kwargs["output"]
        if not os.path.exists(in_tif):
            raise FileNotFoundError(in_tif)
        if not os.path.exists(out_tif):
            raise FileNotFoundError(out_tif)
        # Reading XMP metadata tags from the original image
        tags = GeoTiff(in_tif).xmp_metadata_dict()

        qgis_scripts = self._kwargs["qgis_scripts"] \
            if "qgis_scripts" in self._kwargs else ""

        command = ["python", os.path.join(qgis_scripts, str(GdalCommand.EDIT))]
        for k, v in sorted(tags.items()):
            command.append('-mo')
            command.append('OAW_%s="%s"' % (k.upper(), v.replace('"', "'") if v is not None else ""))
            print('assert "OAW_%s=" in call[%d]' % (k.upper(), len(command)-1))

        command.append(out_tif)
        statement = ' '.join(command)
        gdal_prc = GdalProcess("gdal_edit", ret_out=True, log_location=self._kwargs['log_location'])
        gdal_prc.process(cmd=statement)
