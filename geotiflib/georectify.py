from .utils import Utils
from .eventhook import EventHook


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
            task.set_args(args=self._args, kwargs=self._kwargs)
            task.run()
            progress += step
            self.on_progress.fire({"value": progress})
        progress = 100.0
        self.on_progress.fire({"value": progress})
