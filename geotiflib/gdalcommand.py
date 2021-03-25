from enum import Enum


class GdalCommand(Enum):
    INFO = "gdalinfo"
    TRANSLATE = "gdal_translate"
    WARP = "gdalwarp"
    BUILD_VRT = "gdalbuildvrt"
    CALC_ = "C:\\OSGeo4W64\\apps\\Python37\\python.exe C:\\OSGeo4W64\\apps\\Python37\\Scripts\\gdal_calc.py"
    CALC = "python C:\\OSGeo4W64\\apps\\Python37\\Scripts\\gdal_calc.py"
    ADDO = "gdaladdo"

    def __str__(self):
        return self.value

