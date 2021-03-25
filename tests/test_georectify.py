import os
import mock
from geotiflib.georectify import GeoRectify
from .utils import get_data_folder


def test_constructor():
    process = GeoRectify()
    assert isinstance(process, GeoRectify) is True


@mock.patch('geotiflib.task.basetask.BaseTask')
def test_pipe(mock_task):
    process = GeoRectify()
    assert process == process.pipe(mock_task)
    assert process.task_count() == 1


@mock.patch('geotiflib.task.basetask.BaseTask')
def test_process(mock_task):
    process = GeoRectify()
    process\
        .pipe(mock_task)\
        .pipe(mock_task)
    spy = mock.Mock()
    process.on_progress += spy
    process.process()
    assert spy.called is True
    assert spy.call_count == 4
