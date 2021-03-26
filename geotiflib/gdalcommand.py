from enum import Enum


class GdalCommand(Enum):
    INFO = "gdalinfo"
    TRANSLATE = "gdal_translate"
    WARP = "gdalwarp"
    BUILD_VRT = "gdalbuildvrt"
    CALC = "gdal_calc.py"
    ADDO = "gdaladdo"

    def __str__(self):
        return self.value

