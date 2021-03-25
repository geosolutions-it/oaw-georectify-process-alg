import os

IGNORED_ERRORS = ['ILLEGAL BAND']


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
        #os.environ["CPL_DEBUG"] = 'NO'
        #os.environ["CPL_LOG_ERRORS"] = 'NO'
        #os.environ["CPL_MAX_ERROR_REPORTS"] = '0'
        #os.environ["CPL_ACCUM_ERROR_MSG"] = 'NO'
        return os.environ["GDAL_TIFF_INTERNAL_MASK"] == 'YES'

    @staticmethod
    def make_command(c_name, *args, **kwargs):
        """
        Build command
        :param c_name: command name
        :param args: positional arguments
        :param kwargs: keyword arguments (they will be transformed in key=value)
        :return: command list
        """
        _split = True
        _replacingChar = None
        if kwargs and "split" in kwargs:
            _split = kwargs["split"]
            kwargs.pop("split")
        if kwargs and _split and "replacingChar" in kwargs:
            _replacingChar = kwargs["replacingChar"]
            kwargs.pop("replacingChar")
        cmd = c_name
        if args:
            cmd = "%s %s" % (cmd, " ".join(args))
        if kwargs:
            for key in kwargs:
                values = get_iter_items(kwargs[key])
                options = " ".join(["%s=%s" % (k, v) for k, v in values])
                cmd = "%s %s" % (cmd, options)
        final_command = cmd.split() if _split else cmd
        if _replacingChar:
            for i in range(len(final_command)):
                final_command[i] = final_command[i].replace(_replacingChar, " ")
        for i in range(len(final_command)):
            final_command[i] = final_command[i].replace("|", " ")
        return final_command

    @staticmethod
    def check_output(process_out):
        """
        Check output for errors
        :param process_out: process output
        :return: status, message
        """
        line_output = str(process_out).upper()
        if "ERROR" in line_output or "FAILURE" in line_output:
            for line in line_output.splitlines(True):
                for skip_error in IGNORED_ERRORS:
                    if skip_error not in line.upper():
                        return False, str(process_out)
        return True, None
