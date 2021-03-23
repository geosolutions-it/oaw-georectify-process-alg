import os


class Utils:
    
    @staticmethod
    def is_windows():
        """
        Check if the program is running on Windows
        :return: 
        """
        return os.name == 'nt'

    @staticmethod
    def set_gdal_tiff_mask():
        """
        Set the GDAL_TIFF_INTERNAL_MASK environment variable
        :return: 
        """
        os.environ["GDAL_TIFF_INTERNAL_MASK"] = 'YES'
        return os.environ["GDAL_TIFF_INTERNAL_MASK"] == 'YES'


