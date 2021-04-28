import os
import mock
import pytest
from geotiflib.georectify import GeoRectify, GeoRectifyFactory
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


def test_georecfy_factory_not_implemented():
    with pytest.raises(NotImplementedError) as exc:
        GeoRectifyFactory.create("UNKNOWN")
    assert "Format: UNKNOWN" in str(exc.value)


@mock.patch('subprocess.Popen')
@mock.patch('os.remove')
def test_georecfy_factory(mock_subproc_popen, mock_os_remove):
    process_mock = mock.Mock()
    attrs = {
        'stdout.readlines.return_value': "output",
        'stderr.readlines.return_value': "nothing"
    }
    process_mock.configure_mock(**attrs)
    mock_subproc_popen.return_value = process_mock

    file_tif = os.path.join(get_data_folder(), 'pipe', 'AC04078710.tif')
    process = GeoRectifyFactory.create(input=file_tif)
    assert isinstance(process, GeoRectify) is True
    assert process.task_count() == 9

    spy = mock.Mock()
    process.on_progress += spy
    process.process()
    assert spy.called is True
    assert spy.call_count == 11

"""
def test_georecfy_factory_real():
    file_tif = os.path.join('C:\\geo-solutions\\repositories\\OAW\\data\\XXX', 'AC04078710.tif')
    process = GeoRectifyFactory.create(input=file_tif)

    def on_progress(message):
        print(str(message["value"]))

    process.on_progress += on_progress
    process.process()
"""
