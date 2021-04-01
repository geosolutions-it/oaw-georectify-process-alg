import os
import time
from .basetask import BaseTask


class CleanTask(BaseTask):
    """
    This task will remove intermediate files
    """
    def __init__(self, *args, **kwargs):
        BaseTask.__init__(self, 'CLEAN_TASK', *args, **kwargs)

    def run(self):
        time.sleep(0.2)
        files = self._kwargs["input"]
        for file in files:
            if os.path.exists(file) and os.path.isfile(file):
                os.remove(file)
