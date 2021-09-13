from datetime import datetime
import os
import subprocess
from osgeo import gdal, ogr, osr
from geotiflib.utils import Utils
#from scripts.dsm.process.process import log
from multiprocessing import Value

ogr.UseExceptions()
counter = None


class GdalProcess(object):
    """
    General GDAL process with custom args and kwargs options
    """

    def __init__(self, name, *args, **kwargs):
        self.name = str(name)
        self._args = args
        self._kwargs = kwargs
        def_shell = False
        if Utils.is_windows():
            def_shell = True
        self._shell = self._get_kwarg_value("shell", default=def_shell)
        self._sync = self._get_kwarg_value("sync", default=True)
        self._verbose = self._get_kwarg_value("verbose")
        self._ret_out = self._get_kwarg_value("ret_out")
        self._num_files = self._get_kwarg_value("num_files")
        self._log_location = self._get_kwarg_value("log_location", 'C:\\Users\\alg_log')
        global counter
        counter = Value('i', 0)

    def __call__(self, *args, **kwargs):
        """
        Method called by Pool
        """
        if args and isinstance(args[0], tuple):
            args = args[0]
        self._p_args = self._args + args
        out = self.process()
        if self._ret_out:
            return out

    def _get_kwarg_value(self, key, default=False):
        """
        Retrieve kwargs value from name
        """
        value = default
        if self._kwargs and key in self._kwargs:
            value = self._kwargs[key]
            self._kwargs.pop(key)
        return value

    def process(self, cmd=None):
        """
        Here the subprocess is executed
        """
        Utils.set_gdal_tiff_mask()
        # += operation is not atomic, so we need to get a lock:
        args = self._args if not hasattr(self, "_p_args") else self._p_args
        if cmd is None:
            cmd = Utils.make_command(self.name, *args, **self._kwargs)
        #self._shell = False
        try:
            with counter.get_lock():
                counter.value += 1
                #log.debug("%s (%i/%i)" % (self.name, counter.value, self._num_files))
            print(cmd)
            if not os.path.exists(f"{self._log_location}/log"):
                print(f"not exists: {self._log_location}")
                try:
                    x = os.makedirs(f"{self._log_location}/log")
                    print(x)
                except Exception as e:
                    raise e

            with open(f"{self._log_location}/log/{datetime.today().strftime('%Y%m%d')}", 'a+') as f:
                process = subprocess.Popen(
                    args=cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=f,
                    shell=self._shell
                )
        except Exception as e:
            raise e
        if self._sync:
            out_lines = process.stdout.readlines()
            out = ''.join([str(x) for x in out_lines])
            #err_lines = process.stderr.readlines()
            #err = ''.join([str(x) for x in err_lines])
            #check, msg = Utils.check_output(err)

            #out, _ = process.communicate()
            #check, msg = Utils.check_output(out)

            #if not check:
            #    # Raise command exception
            #    raise Exception("%s - %s" % (self.name, msg))
            if self._verbose:
                #log.debug("%s" % (out))
                pass
            if self._ret_out:
                return out
