import os
from .utils import Utils
from .eventhook import EventHook
from geotiflib.task.addgcptask import AddGcpTask
from geotiflib.task.warptask import WarpTask
from geotiflib.task.separatebandtask import SeparateBandTask
from geotiflib.task.binarymasktask import BinaryMaskTask
from geotiflib.task.recombinebandmasktask import RecombineBandMaskTask
from geotiflib.task.tilejpegtask import TileJpegTask
from geotiflib.task.addoverviewtask import AddOverviewTask
from geotiflib.task.edittagtask import EditTagTask
from geotiflib.task.cleantask import CleanTask


class GeoRectify:

    def __init__(self, *args, **kwargs):
        self._tasks = []
        self._args = args
        self._kwargs = kwargs
        self.on_progress = EventHook()

    def pipe(self, task):
        """
        Adds a task in the georectify image processing and returns itself (chainable method)
        :param task: task to append in the tasks queue
        :return: Georectify
        """
        self._tasks.append(task)
        return self

    def task_count(self):
        """
        Return the number of the tasks in the queue
        :return:
        """
        return len(self._tasks)

    def process(self):
        """
        Execute the georectify process, task by task
        :return:
        """
        Utils.set_gdal_tiff_mask()
        progress = 0.0
        self.on_progress.fire({"value": progress})
        step = 100.0/len(self._tasks) if len(self._tasks) > 0 else 0
        for task in self._tasks:
            #task.set_args(args=self._args, kwargs=self._kwargs)
            task.run()
            progress += step
            self.on_progress.fire({"value": progress})
        progress = 100.0
        self.on_progress.fire({"value": progress})


class GeoRectifyFactory:

    @staticmethod
    def create(mode="OAW_TIF", *args, **kwargs):
        """
        Create the Georectify object
        :param mode: type of the GeoRectify object to create ["OAW_TIF"]
        :param args:
        :param kwargs:
            "input" => path to the tif image to be processed
            "min_points" => minimum number of GCPs in the *.points file (default -1)
            "qgis_scripts" => path the Scripts folder in the QGIS installation
        :return: GeoRectify
        """
        if mode == "OAW_TIF":
            in_tif = kwargs["input"]
            input_folder = os.path.dirname(in_tif)
            output_folder = kwargs["output_folder"] if "output_folder" in kwargs else input_folder
            qgis_scripts = kwargs["qgis_scripts"] \
                if "qgis_scripts" in kwargs else "C:\\OSGeo4W64\\apps\\Python37\\Scripts\\"
            min_points = kwargs["min_points"] if "min_points" in kwargs else -1
            gdal_threads = kwargs["gdal_threads"] if "gdal_threads" in kwargs else 4
            base_name = os.path.basename(in_tif)
            gcp_tif = os.path.join(output_folder, base_name.replace(".tif", "_gcp.tif"))
            grf_tif = os.path.join(output_folder, base_name.replace(".tif", "_grf.tif"))
            bnd_vrt = os.path.join(output_folder, base_name.replace(".tif", "_grf_b{band}.vrt"))
            msk_tif = os.path.join(output_folder, base_name.replace(".tif", "_grf_msk.tif"))
            fin_vrt = os.path.join(output_folder, base_name.replace(".tif", "_grf_fin.vrt"))
            if input_folder == output_folder:
                fin_tif = os.path.join(output_folder, base_name.replace(".tif", "_grf_fin.tif"))
            else:
                fin_tif = os.path.join(output_folder, base_name)
            geo = GeoRectify(*args, **kwargs)
            return geo.pipe(
                AddGcpTask(input=in_tif, output=gcp_tif, min_points=min_points, log_location=input_folder)
            ).pipe(
                WarpTask(input=gcp_tif, output=grf_tif, log_location=input_folder)
            ).pipe(
                SeparateBandTask(input=grf_tif, output=bnd_vrt, log_location=input_folder)
            ).pipe(
                BinaryMaskTask(input=bnd_vrt, output=msk_tif, qgis_scripts=qgis_scripts, gdal_threads=gdal_threads, log_location=input_folder)
            ).pipe(
                RecombineBandMaskTask(input_vrt=bnd_vrt, input_mask=msk_tif, output=fin_vrt, log_location=input_folder)
            ).pipe(
                TileJpegTask(input=fin_vrt, output=fin_tif, log_location=input_folder)
            ).pipe(
                AddOverviewTask(input=fin_tif, log_location=input_folder)
            ).pipe(
                EditTagTask(input=in_tif, output=fin_tif, qgis_scripts=qgis_scripts, log_location=input_folder)
            ).pipe(
                CleanTask(input=[
                    gcp_tif, grf_tif,
                    bnd_vrt.replace("{band}", "1"),
                    bnd_vrt.replace("{band}", "2"),
                    bnd_vrt.replace("{band}", "3"),
                    msk_tif, fin_vrt
                ])
            )
        else:
            raise NotImplementedError("Format: " + mode)
