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
            qgis_scripts = kwargs["qgis_scripts"] \
                if "qgis_scripts" in kwargs else "C:\\OSGeo4W64\\apps\\Python37\\Scripts\\"
            min_points = kwargs["min_points"] if "min_points" in kwargs else -1
            gcp_tif = in_tif.replace(".tif", "_gcp.tif")
            grf_tif = in_tif.replace(".tif", "_grf.tif")
            bnd_vrt = in_tif.replace(".tif", "_grf_b{band}.vrt")
            msk_tif = in_tif.replace(".tif", "_grf_msk.tif")
            fin_vrt = in_tif.replace(".tif", "_grf_fin.vrt")
            fin_tif = in_tif.replace(".tif", "_grf_fin.tif")

            geo = GeoRectify(*args, **kwargs)
            return geo.pipe(
                AddGcpTask(input=in_tif, output=gcp_tif, min_points=min_points)
            ).pipe(
                WarpTask(input=gcp_tif, output=grf_tif)
            ).pipe(
                SeparateBandTask(input=grf_tif, output=bnd_vrt)
            ).pipe(
                BinaryMaskTask(input=bnd_vrt, output=msk_tif, qgis_scripts=qgis_scripts)
            ).pipe(
                RecombineBandMaskTask(input_vrt=bnd_vrt, input_mask=msk_tif, output=fin_vrt)
            ).pipe(
                TileJpegTask(input=fin_vrt, output=fin_tif)
            ).pipe(
                AddOverviewTask(input=fin_tif)
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
