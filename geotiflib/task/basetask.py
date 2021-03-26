

class BaseTask:

    def __init__(self, name, *args, **kwargs):
        self._name = name
        self._args = args
        self._kwargs = kwargs

    def set_args(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def run(self):
        raise NotImplementedError
