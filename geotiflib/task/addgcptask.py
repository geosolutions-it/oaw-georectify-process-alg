import os
from .basetask import BaseTask
from ..gcpreader import GCPReader
from ..gdalprocess import GdalProcess
from ..gdalcommand import GdalCommand


class AddGcpTask(BaseTask):
    """
    This task will add gcp points in an itermediate tif file
    Example of the command:
    gdal_translate -of GTiff -co
        -gcp 8540.91 4987.66 1822331.48 6141557.76
        -gcp 1444.15 1180.69 775208.37 6610054.25
        AC04078710.tif AC04078710_gcp.tif
    """

    def __init__(self, *args, **kwargs):
        BaseTask.__init__(self, 'ADD_GCP_TASK', *args, **kwargs)

    def run(self):
        in_image = self._kwargs["input"]
        in_points = in_image + ".points"
        out_image = self._kwargs["output"]
        min_points = self._kwargs["min_points"] if 'min_points' in self._kwargs else -1
        if os.path.exists(in_image) and os.path.isfile(in_image):
            if os.path.exists(in_points) and os.path.isfile(in_points):
                reader = GCPReader(in_points)
                if reader.parse():
                    gcp_count = reader.count()
                    if min_points == -1 or reader.count() >= min_points:
                        gdal_prc = GdalProcess(
                            GdalCommand.TRANSLATE,
                            "-of GTiff",
                            reader.get_list_as_string(),
                            in_image, out_image,
                            ret_out=True, log_location=self._kwargs['log_location'])
                        result = gdal_prc.process()
                    else:
                        raise ImportError("Insufficient number of GCPs: %d < %d" % (gcp_count, min_points))
                else:
                    raise ImportError("Unable to parse GCPs file: " + in_points)
            else:
                raise FileNotFoundError(in_points)
        else:
            raise FileNotFoundError(in_image)
